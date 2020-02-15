#! python 3
#! utf-8

import bs4
import datetime
import getpass
import re
import requests

from selenium import webdriver
from helper_functions import *

# Variables
moodleURL = "https://moodle.s.kyushu-u.ac.jp/"
loginURL = "https://moodle.s.kyushu-u.ac.jp/login/index.php"
"""
====== Automation of Attendance Taking on Moodle =====
| Timetable |
- excel file
- editable by user

| Timetable (csv) |
- read-only (user)
- generated / updated with Python based on Timetable
- has same content with Timetable (excel) but also comes with Subject ID
"""


if __name__ == "__main__":
    print('Hello')

    # 0. Get System Arguments
        # Update Timetable
        # Register Course on Moodle
        # if no arguments, take attendance
    # Get username and Password
    username = input('Username: ')
    pw = getpass.getpass('Password: ')
    # Access Moodle Log In Page
    browser = webdriver.Firefox()
    browser.get(loginURL)
    # Log In
    login(browser, username, pw)

    # 3. Access Course Page
    # 4. Access Attentance Page (of the Course)
    # 5. Take Attendance

    # Quit
    browser.quit()
