import json
import random
import time
import seleniumwire.undetected_chromedriver as uc
import datetime
import os
from person import Person
from faker import Faker
from util import decompress_if_gzip, decode_and_parse_json, read_env
from seleniumwire import webdriver
from phone_gen import PhoneNumber


def get_random_addresses_by_state(driver: webdriver, state: str, sleep_for: int = 3, proxy=None):
    url = f"https://{state.strip().lower()}.postcodebase.com/randomaddress"
    driver.get(url)
    time.sleep(sleep_for)
    for request in driver.requests:
        if request.response:
            if (
                    request.url == 'https://zip.postcodebase.com/api/random_address.php'
                    and request.response.status_code == 200
                    and request.method == 'POST'
            ):
                data = decode_and_parse_json(decompress_if_gzip(request.response.body))
                return data['data']
    return None


def read_names_from_file(file_path='names.json'):
    with open(file_path, 'r') as f:
        names = json.load(f)
    first_last_names = []
    for name in names:
        first_and_last = name.split(' ')
        first_last_names.append(
            {
                'first': first_and_last[0],
                'last': ' '.join(first_and_last[1:])

            }
        )
    return first_last_names


def write_addresses_to_file(addresses, file_path='addresses.json'):
    with open(file_path, 'w') as f:
        json.dump(addresses, f, indent=4)


def read_addresses_from_file(file_path='addresses.json'):
    with open(file_path, 'r') as f:
        addresses = json.load(f)
    return addresses


def build_chrome_options(proxy=None):
    chrome_options = uc.ChromeOptions()
    proxy = proxy if proxy else {}
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--headless')
    driver = uc.Chrome(
        options=chrome_options,
        seleniumwire_options={
            'verify_ssl': False,
            'proxy': proxy
        }
    )
    return driver


def get_addresses(sleep_for: int = 3, proxy: dict = None):
    print("Getting random addresses... Please wait...")
    states = ['PA', 'GA', 'NV', 'AZ', 'WI', 'MI', 'NC']
    driver = build_chrome_options(proxy)

    raw_addresses = get_random_addresses_by_state(driver, random.choice(states), sleep_for)
    addresses = []

    if raw_addresses is None:
        print("No addresses found.")
        driver.quit()
        return addresses

    for raw_address in raw_addresses:
        full = raw_address['zip']
        if raw_address['predirect'] and raw_address['predirect'].strip() != '':
            full = f"{full} {raw_address['predirect']}"
        if raw_address['streetname'] and raw_address['streetname'].strip() != '':
            full = f"{full} {raw_address['streetname']}"
        if raw_address['suffix'] and raw_address['suffix'].strip() != '':
            full = f"{full} {raw_address['suffix']}"
        full = f"{full}, {raw_address['cityname']}, {raw_address['stateabbr']} {raw_address['zipcodeplus4'].split('-')[0]}, {raw_address['country']}"
        address = {
            'number': raw_address['zip'],
            'street': f"{raw_address['predirect']} {raw_address['streetname']} {raw_address['suffix']}".strip(),
            'city': raw_address['cityname'],
            'state': raw_address['stateabbr'],
            'zip': raw_address['zipcodeplus4'].split('-')[0],
            'country': raw_address['country'],
            'full': full
        }
        addresses.append(address)
    driver.quit()
    return addresses


def save_people_to_file(people, file_path='people.json'):
    try:
        with open('people.json', 'r') as f:
            people += [Person(**person) for person in json.load(f)]
    except FileNotFoundError:
        pass
    with open('people.json', 'w') as f:
        json.dump([person.__dict__() for person in people], f, indent=4)


def count_saved_people(file_path='people.json'):
    try:
        with open('people.json', 'r') as f:
            return len(json.load(f))
    except Exception:
        return 0


def move_file_to_on_deck(file_path: str):
    # rename the file to include the current date and time
    os.rename(file_path,
              f'on-deck/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{os.path.basename(file_path)}')


def main():
    while True:
        config = read_env()
        proxy = None
        count = count_saved_people()
        if config['use_proxy']:
            proxy_auth = f"{config['proxy_user']}:{config['proxy_pass']}@" if config['proxy_auth'] else ''
            proxy_scheme_http = 'http' if config['proxy_type'] == 'http' else config['proxy_type']
            proxy_scheme_https = 'https' if config['proxy_type'] == 'http' else config['proxy_type']
            proxy = {
                'http': f"{proxy_scheme_http}://{proxy_auth}{config['proxy_host']}:{config['proxy_port']}",
                'https': f"{proxy_scheme_https}://{proxy_auth}{config['proxy_host']}:{config['proxy_port']}",
                'no_proxy': 'localhost,127.0.0.1'
            }

        addr_proxy = proxy if config['use_proxy'] else None

        names = read_names_from_file()

        phone_generator = PhoneNumber('USA')
        email_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com', 'mail.com']
        fake = Faker(locale='en_US')

        while count < config['people_to_generate']:
            people = []
            try:
                addresses = get_addresses(sleep_for=config['sleep_for_addresses'], proxy=addr_proxy)
            except Exception as e:
                print('Error getting addresses:', e)
                addresses = []
                time.sleep(5)

            for address in addresses:
                phone = phone_generator.get_number(full=False)
                name = random.choice(names)
                email = (
                        fake.word() +
                        (('' if random.choice([True, False]) else '-') +
                         fake.word() if random.choice([True, False]) else '') +
                        (('' if random.choice([True, False]) else '-') +
                         fake.word() if random.choice([True, False]) else '') +
                        str(fake.random_number(digits=(random.randint(1, 5)))) +
                        '@' + random.choice(email_domains)
                )
                my_person = Person(
                    first_name=name['first'],
                    last_name=name['last'],
                    address=address,
                    phone_number=phone,
                    email=email
                )
                print('Constructed', my_person.__repr__())
                people.append(my_person)
            save_people_to_file(people)
            count = count_saved_people()
            print(f"Generated {count} people.")

        move_file_to_on_deck('people.json')
        print("Moved file to 'on_deck' folder.")
        print("Sleeping for 2 seconds...")
        time.sleep(2)



if __name__ == '__main__':
    main()
