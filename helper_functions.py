#! python 3
#! utf-8

import getpass
import pandas as pd
import re
import requests
import sys

from bs4 import BeautifulSoup

""" Variables """
moodleURL = "https://moodle.s.kyushu-u.ac.jp/"
loginURL = "https://moodle.s.kyushu-u.ac.jp/login/index.php"
courseURL = "https://moodle.s.kyushu-u.ac.jp/course/view.php?id=" # add course ID at the end

headers = {
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0"
}

""" Common Functions """
def login(session):
    req = session.get(loginURL, headers=headers)
    print(req.status_code) # 200 if okay
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
    if (res.status_code == requests.codes.ok):
        print('Logged In')
        # return soup of page after login
        return True
    else:
        print('Failed to log in.')
        return False

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
        # Login
        loggedIn = login(s)
        if loggedIn:
            # get Timetable
            timetable = pd.read_csv('data/timetable.csv')
            # Check Attendance
            now = {
                'year': 2020,
                'month': 2,
                'day': 4,
                'weekofday': 1,
                'period': 1
            }
            courseID = timetable.loc[(timetable['Week of Day'] == now['weekofday']) &
                                     (timetable['Period'] == now['period']), 'ID'].values[0]
            course_req = s.get(courseURL + str(courseID))
            print(course_req.status_code)


def search():
    pass
