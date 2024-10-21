import pyautogui
import cv2
import numpy as np
from PIL import ImageGrab
import time
import json
import os
import platform
import datetime
import random
from util import read_env


# Take a screenshot of the entire screen
def take_screenshot():
    screenshot = ImageGrab.grab()
    screenshot_np = np.array(screenshot)  # Convert to numpy array
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)  # Convert to BGR
    return screenshot_np


# Locate element by matching template (reference image)
def find_element(template_path, screenshot):
    template = cv2.imread(template_path, 0)  # Load template image in grayscale
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)  # Convert screenshot to grayscale

    # Match template with the screenshot
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)

    # Get the location of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Define a threshold for matching
    threshold = 0.98
    if max_val >= threshold:
        return max_loc  # Return the top-left corner of the match
    else:
        return None  # No match found


# Move mouse to the found element and click
def move_and_click(position, retina_display=False):
    x, y = position
    pyautogui.moveTo(
        x / (2 if retina_display else 1) + random.randint(23, 30),
        y / (2 if retina_display else 1) + random.randint(20, 25),
        duration=0.5
    )
    pyautogui.click()

def move_and_click_manual_address_button(position, retina_display=False):
    x, y = position
    pyautogui.moveTo(
        x / (2 if retina_display else 1) + random.randint(23, 30),
        y / (2 if retina_display else 1) + random.randint(1, 3),
        duration=0.5
    )
    pyautogui.click()

def move_and_click_address_from_dropdown(position, retina_display=False):
    x, y = position
    pyautogui.moveTo(
        x / (2 if retina_display else 1) + random.randint(23, 30),
        y / (2 if retina_display else 1) + random.randint(58, 63),
        duration=0.5
    )
    pyautogui.click()


def move_and_click_sign_button(position, retina_display=False):
    x, y = position
    pyautogui.moveTo(
        x / (2 if retina_display else 1) + random.randint(23, 90),
        y / (2 if retina_display else 1) + random.randint(25, 45),
        duration=0.5
    )
    pyautogui.click()


def move_and_click_captcha_button(position, retina_display=False):
    x, y = position
    pyautogui.moveTo(
        x / (2 if retina_display else 1) + random.randint(23, 90),
        y / (2 if retina_display else 1) + random.randint(25, 45),
        duration=0.5
    )
    pyautogui.click()


def center_mouse(retina_display=False):
    screen_width, screen_height = pyautogui.size()
    # Calculate center coordinates
    center_x = screen_width / (2 if retina_display else 1)
    center_y = screen_height / (2 if retina_display else 1)
    # Move mouse to center
    pyautogui.moveTo(center_x, center_y)


def read_people(file_path: str):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception:
        return 0


def list_files():
    files = []
    for file in os.listdir('on-deck'):
        if file.endswith('.json'):
            files.append(file)
    return files


# Move file to the 'done' folder
def move_file_to_done(file_path: str):
    # rename the file to include the current date and time
    os.rename(file_path, f'done/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_{os.path.basename(file_path)}')


def random_micro_sleep(min_sleep=0.3, max_sleep=0.8):
    time.sleep(random.uniform(min_sleep, max_sleep))


def main():
    time.sleep(5)  # Wait for 5 seconds before taking the screenshot
    # Define the reference images for the form fields
    first_name_ref = 'screens/first_name.png'
    last_name_ref = 'screens/last_name.png'
    email_ref = 'screens/email.png'
    phone_ref = 'screens/cell_phone.png'
    address_ref = 'screens/address.png'
    cf_capcha_ref = 'screens/cf_capcha_1.png'
    cf_capcha_ref_2 = 'screens/cf_capcha_2.png'
    sign_button_1_ref = 'screens/sign_button_1.png'
    sign_button_2_ref = 'screens/sign_button_2.png'
    sign_button_3_ref = 'screens/sign_button_3.png'
    sign_button_4_ref = 'screens/sign_button_4.png'
    use_manual_address_ref = 'screens/manual_address.png'
    street_address_ref = 'screens/street_address.png'
    city_ref = 'screens/city.png'
    zip_ref = 'screens/zip.png'
    state_dropdown_ref = 'screens/state_dropdown.png'

    # The number of down arrow presses to get to the desired state in the dropdown
    az = 3
    ga = 11
    mi = 23
    nv = 29
    nc = 34
    pa = 39
    wi = 50

    while True:
        config = read_env()
        pyautogui.FAILSAFE = config['enable_failsafe']
        retina_display = config['retina_display']
        people_files = list_files()

        for file in people_files:
            people = read_people(f'on-deck/{file}')
            for person in people:
                print(person)
                center_mouse(retina_display)
                random_micro_sleep()

                # Open a new tab in the browser
                # If macOS, use 'command' instead of 'ctrl'
                if platform.system().lower() == 'darwin':
                    pyautogui.keyUp('fn')
                    pyautogui.hotkey('command', 't')
                else:
                    pyautogui.hotkey('ctrl', 't')

                random_micro_sleep()
                # Type the URL of the petition website
                pyautogui.typewrite('https://petition.theamericapac.org/')
                pyautogui.press('enter')
                random_micro_sleep()
                random_micro_sleep()

                center_mouse(retina_display)
                random_micro_sleep()
                # scroll down
                pyautogui.scroll(-500)

                # take screenshot
                screenshot = take_screenshot()

                # find the first name field
                first_name_pos = find_element(first_name_ref, screenshot)
                if not first_name_pos:
                    print('First name field not found!')
                    continue
                move_and_click(first_name_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['first_name'].capitalize())

                # find the last name field
                last_name_pos = find_element(last_name_ref, screenshot)
                if not last_name_pos:
                    print('Last name field not found!')
                    continue
                move_and_click(last_name_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['last_name'].capitalize())

                # find the email field
                email_pos = find_element(email_ref, screenshot)
                if not email_pos:
                    print('Email field not found!')
                    continue
                move_and_click(email_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['email'])

                # find the phone field
                phone_pos = find_element(phone_ref, screenshot)
                if not phone_pos:
                    print('Phone field not found!')
                    continue
                move_and_click(phone_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['phone_number'])

                # find the manual address button
                manual_address_pos = find_element(use_manual_address_ref, screenshot)
                if not manual_address_pos:
                    print('Manual address button not found!')
                    continue
                move_and_click_manual_address_button(manual_address_pos, retina_display)
                random_micro_sleep()
                random_micro_sleep()
                random_micro_sleep()
                screenshot = take_screenshot()

                # # Find the street address input
                # street_address_pos = find_element(address_ref, screenshot)
                # if not street_address_pos:
                #     print('Street address field not found!')
                #     continue
                # move_and_click(street_address_pos, retina_display)
                # random_micro_sleep()
                pyautogui.typewrite(str(person['address']['number'] + ' ' + person['address']['street']).capitalize())

                # Find the city input
                city_pos = find_element(city_ref, screenshot)
                if not city_pos:
                    print('City field not found!')
                    continue
                move_and_click(city_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['address']['city'].capitalize())

                # Find the state dropdown
                state_dropdown_pos = find_element(state_dropdown_ref, screenshot)
                if not state_dropdown_pos:
                    print('State dropdown not found!')
                    continue
                move_and_click(state_dropdown_pos, retina_display)
                random_micro_sleep()

                if person['address']['state'] == 'AZ':
                    for _ in range(az):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'GA':
                    for _ in range(ga):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'MI':
                    for _ in range(mi):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'NV':
                    for _ in range(nv):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'NC':
                    for _ in range(nc):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'PA':
                    for _ in range(pa):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                elif person['address']['state'] == 'WI':
                    for _ in range(wi):
                        pyautogui.press('down')
                        random_micro_sleep(min_sleep=0.008, max_sleep=0.05)
                else:
                    print('State not found!')
                    continue
                pyautogui.keyUp('fn')
                pyautogui.press('enter')

                # find the zip field
                zip_pos = find_element(zip_ref, screenshot)
                if not zip_pos:
                    print('Zip field not found!')
                    continue
                move_and_click(zip_pos, retina_display)
                random_micro_sleep()
                pyautogui.typewrite(person['address']['zip'])

                # find the capcha field
                capcha_pos = find_element(cf_capcha_ref, screenshot)
                capcha_pos_2 = find_element(cf_capcha_ref_2, screenshot)

                if capcha_pos_2:
                    print('Capcha 2 field found... attempting to solve.')
                    move_and_click(capcha_pos_2, retina_display)
                    random_micro_sleep()
                    pyautogui.scroll(-500)
                    random_micro_sleep()
                    screenshot = take_screenshot()
                elif capcha_pos:
                    print('Capcha 1 field found... attempting to solve.')
                    move_and_click_captcha_button(capcha_pos, retina_display)
                    random_micro_sleep()
                    pyautogui.scroll(-500)
                    random_micro_sleep()
                    screenshot = take_screenshot()
                else:
                    print('Capcha field not found.')

                # find the sign button
                sign_1_pos = find_element(sign_button_1_ref, screenshot)
                sign_2_pos = find_element(sign_button_2_ref, screenshot)
                sign_3_pos = find_element(sign_button_3_ref, screenshot)
                sign_4_pos = find_element(sign_button_4_ref, screenshot)

                if sign_1_pos:
                    print('Sign button 1 found!')
                    move_and_click_sign_button(sign_1_pos, retina_display)
                elif sign_2_pos:
                    print('Sign button 2 found!')
                    move_and_click_sign_button(sign_2_pos, retina_display)
                elif sign_3_pos:
                    print('Sign button 3 found!')
                    move_and_click_sign_button(sign_3_pos, retina_display)
                elif sign_4_pos:
                    print('Sign button 4 found!')
                    move_and_click_sign_button(sign_4_pos, retina_display)
                else:
                    print('Sign button not found!')
                    continue
                random_micro_sleep()
                random_micro_sleep()

                # close the tab
                if platform.system().lower() == 'darwin':
                    pyautogui.keyUp('fn')
                    pyautogui.hotkey('command', 'w')
                else:
                    pyautogui.hotkey('ctrl', 'w')

            random_micro_sleep()
            move_file_to_done(f'on-deck/{file}')
        print("Sleeping for 2 seconds...")
        time.sleep(2)


if __name__ == "__main__":
    main()
