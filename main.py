#! python 3
#! utf-8

import bs4
import datetime
import getpass
import re
import requests
import sys

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
    # get argument from terminal
    task = sys.argv[1:2] # this decides what the program will do
    if len(task) == 0:
        print('Usage: python main.py <feature>.')
        print("""
            Features currently available:
            1. Automatic Attendance <attend>
            2. Search for a Subject <search>
        """)
    else:
        if (task == 'attend'):
            attend()
        elif (task == 'search'):
            search()
        else:
            print("That feature is currently not available.\nPlease try it again.")
