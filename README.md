# Stupid Fucking Petition Fillerupper

A stupid script to fill up [this stupid fucking petition](https://petition.theamericapac.org/) with stupid garbage data.

![in action](in_action.gif "In Action")

### You can stop the script by bringing your mouse to any corner of the screen.

## Prerequisites

* Google Chrome
* Chromedriver (Yes, it's a garbage Selenium script)

## Environment

* I've only tested this on macOS, it might work on Windows and Linux, but I'm not sure.
* I've only tested with python 3.12
* Chromedriver was installed through Homebrew
* Chrome was installed through Homebrew

## How it works

There are two scripts. `generate_people.py` and `fill_form.py`.

### `generate_people.py`

This script runs in a loop creating fake people. It uses Selenium and Chromedriver to scrape a webpage with addresses.
It then generates fake people and stores them in a JSON file in `people.json`. Once the configured `PEOPLE_TO_GENERATE`
threshold has been reached `people.json` is moved to `on-deck/$(date)_people.json`. This runs in a loop until you kill
the script.

### `fill_form.py`

This script automates filling out the petition with the people you've generated with `generate_people.py`. It uses
PyAutoGUI to click around the screen and fill out the form. It looks for files in the `on-deck/` directory and fills out
the petition with the people in the file. Once the script has looped through all the people in the file it moves the
file
to the `done/` directory. It then looks for the next file in the `on-deck/` directory and repeats the process. This runs
in a loop until you kill the script.

### `.env`

This is where you configure the scripts

* `RETINA_DISPLAY` - If you're using a retina display set this to `true` otherwise set it to `false`.
* `PEOPLE_TO_GENERATE` - The number of people to generate before moving the `people.json` file to `on-deck/`.
* `SLEEP_FOR_ADDRESSES` - The number of seconds to sleep between making requests to the site to scrape mailing
  addresses.
* `USE_PROXY` - Enable the use of a proxy when you scrape mailing addresses.
* `PROXY_AUTH` - Enable the use of a proxy with authentication. If you set this to `true` you must set `PROXY_USER` and
  `PROXY_PASS`.
* `PROXY_HOST` - The proxy ip or hostname to connect to.
* `PROXY_PORT` - The proxy port to connect to.
* `PROXY_USER` - The proxy username if authentication is required.
* `PROXY_PASS` - The proxy password if authentication is required.
* `PROXY_TYPE` - The proxy protocol to use. Valid options would be: `http`, `socks4`, `socks5`, or `socks5h`.

## Setup

Clone the repository

```bash
git clone https://github.com/06caveattofu/Stupid-Fucking-Petition-Fillerupper.git
```

Change directory to the project directory

```bash
cd Stupid-Fucking-Petition-Fillerupper
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment on Windows

```bash
source env/Scripts/activate
```

Activate the virtual environment on Linux or Mac

```bash
source env/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create the `.env` file, `names.json` file, and `screens/` directory.

```bash
cp example.env .env
cp names.example.json names.json
cp -r screens-example/ screens/
```

Edit `.env` as you see fit.

Add or remove names from `names.json` as you see fit.

If you need to update screenshots to better match webpage elements on the petition then replace them in the `screens/`
folder.

## Running It

Open a terminal and run `generate_people.py`

```bash
python generate_people.py
```

Open Chrome, you don't need to navigate to the petition, just leave it open and ensure it's in the foreground. Then open
a terminal and run `fill_form.py`. Click on the Chrome window to ensure it's in the foreground.

```bash
python fill_form.py
```

You'll probably run into issues. This is buggy garbage code. Good luck.
