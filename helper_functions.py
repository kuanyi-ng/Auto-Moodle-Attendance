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

""" Common Functions """
def login(session, req):
    # information needed for login
    login_data = {
        'logintoken': '',
        'username': input("Username: "),
        'password': getpass.getpass("Password: ")
    }
    # Find login token
    soup = BeautifulSoup(req.text, 'lxml')
    token = soup.find_all('input', attrs={'name':'logintoken'})
    login_data['logintoken'] = token[0]['value']

    # login
    res = session.post(loginURL, data=login_data, headers=headers)

    print(res.status_code)
    print('Logged In')
    # return soup of page after login
    return BeautifulSoup(res.text, 'lxml')


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
        print(req.status_code) # 200 if okay

        # Login
        home_soup = login(s, req)

def search():
    pass
