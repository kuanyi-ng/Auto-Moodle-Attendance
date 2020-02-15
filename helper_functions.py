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

day_ref = {0: '月', 1: '火' , 2: '水', 3: '木', 4: '金'}
attendance_ref = {'欠': 0, '出': 1}

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
    if (res.status_code == requests.codes.ok): # TODO: not a good check for success login
        print('Logged In')
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
    with requests.Session() as session:
        # Login
        loggedIn = login(session)
        if loggedIn:
            # get Timetable
            timetable = pd.read_csv('data/timetable.csv')
            # Get current date and time
            # TODO: Need to deal with situation where classes are held on other day
            now = {
                'year': 2020,
                'month': 2,
                'day': 4,
                'dayofweek': 1,
                'period': 1
            }
            date = f"{str(now['month']).rjust(2, '0')}月{str(now['day']).rjust(2, '0')}日({day_ref[now['dayofweek']]})"
            courseID = timetable.loc[(timetable['Week of Day'] == now['dayofweek']) &
                                     (timetable['Period'] == now['period']), 'ID'].values[0]
            course_req = session.get(courseURL + str(courseID))

            course_soup = BeautifulSoup(course_req.text, 'lxml')
            attendanceURL = course_soup.find_all("a", string="詳細 ...")[0].get('href')
            attendance_req = session.get(attendanceURL)
            attendance_soup = BeautifulSoup(attendance_req.text, 'lxml')

            attendance = attendance_soup.find("td", class_='c1', string=date).find_next_sibling("td", class_='c6')

            while (attendance_ref[attendance.string] != 1):
                # TODO: refresh until it changes
            print('Attendance Taken')

def search():
    pass
