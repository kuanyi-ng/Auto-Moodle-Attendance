#! python 3
#! utf-8

import bs4
import datetime
import re
import requests
import selenium

from helper_functions import *

# Variables
moodleURL = "https://moodle.s.kyushu-u.ac.jp/"

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
    # 1. Access Moodle
    # 2. Log In
    # 3. Access Course Page
    # 4. Access Attentance Page (of the Course)
    # 5. Take Attendance
