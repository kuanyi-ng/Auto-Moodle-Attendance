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
searchURL = "https://moodle.s.kyushu-u.ac.jp/course/search.php?search=" # add possible course name at the end

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

def findId(href):
    # Filtering searched html
    return href and re.compile("view.php\?id=\d\d\d\d\d").search(href)

def search(searchInput):
    """
     1. Do a search by course's name or course id
     2. If wrong input was given:
        -> search & show the all possible results to user.
        -> from user's input above, add it to a searched database(maybe?)
        -> if no possible result was found, throw exception
    3. Return a dictionary of course name & course id
    """

    searchInput = str(searchInput)

    course_name = []
    course_id = []

    try:
        with requests.Session() as session:
            logged = login(session)

            if logged:

                # if searchInput == possible name
                search_result = session.post(searchURL + searchInput).text
                search_soup = BeautifulSoup(search_result, 'lxml')
                course_tags = search_soup.find_all(href=findId)

                # if searchInput == possible course name
                search_result = session.post(searchURL + searchInput).text
                search_soup = BeautifulSoup(search_result, 'lxml')
                course_tags = search_soup.find_all(href=findId)

                # find the course from search results
                for courses in course_tags:
                    for course in courses.find_all('span', attrs={'class', 'highlight'}):
                        course_name.append(courses.text)

                # if searchInput was == id
                if course_name == []:
                    course_tags = session.post(courseURL + searchInput).text
                    result_soup = BeautifulSoup(course_tags, 'lxml')
                    course_info = result_soup.find_all(href=findId)[0]
                    course_name.append(course_info)

                    if course_name == []:
                        print(f"Cannot find {searchInput}!")

                else :
                    # find the class id
                    tmp = []
                    for tag in course_name:
                        tmp.append(str(tag))

                    for name in tmp:
                        course_id.append(name[69:74])

    except Exception:
        print("Cannot connect to website!\nPlease check connection again or Try Again.")

    return dict( zip(course_name, course_id) )
