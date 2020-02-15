#! python 3
#! utf-8

import getpass
import re
import requests
import sys

from bs4 import BeautifulSoup

""" Variables """
moodleURL = "https://moodle.s.kyushu-u.ac.jp/"
loginURL = "https://moodle.s.kyushu-u.ac.jp/login/index.php"

headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0"
}
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

def attend():
    with requests.Session() as s:
        req = s.get(loginURL, headers=headers)
        print(req.status_code)

def search():
    pass
