#! python 3
#! utf-8

import datetime
import getpass
import json
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

day_ref_en = {0: 'Mon', 1: 'Tue' , 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
day_ref = {0: '月', 1: '火' , 2: '水', 3: '木', 4: '金', 5: '土', 6: '日'}
day_ref_jap_en = {'月': 'Mon' , '火': 'Tue'  , '水': 'Wed', '木': 'Thu', '金': 'Fri', '土': 'Sat' , '日': 'Sun'}
attendance_ref = {'欠': 0, '出': 1, '遅': 2}

""" Common Functions """
def doTimetableExist():
    try:
        print("Checking if timetable exist...")
        open('data/timetable.json')
    except FileNotFoundError:
        print("Timetable.json is not found.")
        # create empty json file
        empty = {
            "course": None,
            "lecturer": None,
            "id": None
        }
        print("Creating timetable.json ...")
        with open('data/timetable.json', 'w') as jsonFile:
            emptyTimetable = {"weekday": {}}
            for day in ["Mon", "Tue", "Wed", "Thu", "Fri"]:
                emptyTimetable["weekday"][day] = { str(n): empty for n in range(1, 6) }
            json.dump(emptyTimetable, jsonFile)
        print("timetable.json is created.")

def login(session):
    req = session.get(loginURL, headers=headers)

    if (req.status_code != 200):
        raise Exception("ERROR: Couldn't connect to Moodle")

    # 200 if okay
    print("Connected to Moodle")
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
"""

def get_period(hour, minute):
    # Period 5 to Period 1
    if (hour >= 16):
        if (minute >= 40):
            return 5
        elif (minute <= 20):
            return 4
        else:
            return -1
    elif (hour >= 14):
        if (minute >= 50):
            return 4
        elif (minute <= 30):
            return 3
        else:
            return -1
    elif (hour >= 13):
        return 3
    elif (hour >= 10):
        if (minute >= 30):
            return 2
        elif (minute <= 10):
            return 1
        else:
            return -1
    elif (hour >= 8):
        if (minute < 40):
            return -1
        else:
            return 1
    else:
        return -1

def get_date(datetime_data):
    return f"{str(datetime_data['month']).rjust(2, '0')}月{str(datetime_data['day']).rjust(2, '0')}日({day_ref[datetime_data['weekday']]})"

def get_datetimeData(abnormal=False):
    now = datetime.datetime.now()
    return {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'weekday': int(input("Week of Day (this Course): ")) if abnormal else now.weekday(),
        'period': int(input("Period (this Course): ")) if abnormal else get_period(now.hour, now.minute)
    }

def get_timetableData(datetime_data, info):
    # load json file
    with open("data/timetable.json", "r") as jsonFile:
        timetable = json.load(jsonFile)

    weekOfDay = day_ref_en[datetime_data['weekday']] # str
    period = str(datetime_data['period']) # str

    if (period == '-1'):
        return None
    else:
        return timetable['weekday'][weekOfDay][period][info]

def get_attendanceURL(course_soup):
    try:
        attendanceLink = course_soup.find_all("a", string="詳細 ...")[0]
        return attendanceLink.get('href')
    except IndexError:
        return ""

def get_attendanceStatus(attendance_soup, date):
    try:
        attendanceElem = attendance_soup.find("td", class_='c1', string=date).find_next_sibling("td", class_='c6')
        return attendance_ref[attendanceElem.string]
    # date doesn't exist in attendance table
    except AttributeError: # no class today
        return -1

def attend(replace=False):
    with requests.Session() as session:
        # Login
        loggedIn = login(session)
        if loggedIn:
            # Get current date and time
            datetime_data = get_datetimeData(replace)
            date = get_date(datetime_data)
            # get Course ID
            courseID = get_timetableData(datetime_data, 'id')
            if (courseID != None):
                course_soup = BeautifulSoup(session.get(courseURL + str(courseID)).text, 'lxml')
                # get the URL to enter page with attendance details
                attendanceURL = get_attendanceURL(course_soup)
                if (len(attendanceURL) > 0):
                    attendance_soup = BeautifulSoup(session.get(attendanceURL).text, 'lxml')
                    attendance_status = get_attendanceStatus(attendance_soup, date)

                    limit = 0
                    while ((attendance_status == 0) and (limit <= 100)):
                        attendance_soup = BeautifulSoup(session.get(attendanceURL).text, 'lxml')
                        attendance_status = get_attendanceStatus(attendance_soup, date)
                        limit += 1

                    if (attendance_status == -1):
                        print(f"{get_timetableData(datetime_data, 'course')} doesn't have class today.")
                        print("Otherwise, there might be mistake(s) in the user input or in the date appeared on Moodle.")
                    elif (attendance_status == 1):
                        print(f"Attendance Taken: {get_timetableData(datetime_data, 'course')}")
                    elif (attendance_status == 2):
                        print(f"Attendance (Late) Taken: {get_timetableData(datetime_data, 'course')}")
                    else:
                        print('Attendance Not Taken as limit is exceeded.\nPlease try it again later.')
            else:
                print("Error.")
                print("""
                    Reason: (One of the below)
                    1. No class today
                    2. Course isn't register (with this program)
                """)

"""
====== Search for Course on Moodle =====
"""

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
                    for tag in course_tags:
                        tmp.append(str(tag))

                    for name in tmp:
                        course_id.append(name[69:74])

    except Exception:
        print("Cannot connect to website!\nPlease check connection again or Try Again.")


    # print( dict( zip(course_name, course_id) ) )
    return dict( zip(course_name, course_id) )

"""
====== Register for Course on Moodle =====
"""

def get_RegisterData(course_fullName, id):
    """
    example of course_fullName, 2020年度前期・木3木4・プログラミング基礎（伊藤　浩史）
    regex for this:
    """
    _, dayPeriodPart, coursePart = course_fullName.split(u'\u30FB') # split by・

    dayPeriodMatch = re.split(r'(.{1}\d)', dayPeriodPart)
    while ('' in dayPeriodMatch): # clean dayPeriodMatch
        dayPeriodMatch.remove('')

    courseMatch = re.search(r'(.*)(\uff08.*\uff09)', coursePart)

    return {
        "weekday": [d[0] for d in dayPeriodMatch],
        "period": [d[1] for d in dayPeriodMatch],
        "course": courseMatch.group(1),
        "lecturer": courseMatch.group(2),
        "id": id
    }

def register(course_fullName, id):
    courseToRegister = get_RegisterData(course_fullName, id)
    # read json file
    with open("data/timetable.json", "r") as jsonFile:
        timetable = json.load(jsonFile)
    # check for conflicts
    for i in range(len(courseToRegister["weekday"])):
        weekOfDay = day_ref_jap_en[courseToRegister["weekday"][i]]
        period = courseToRegister["period"][i]
        # other course are registered in this slot
        if (timetable["weekday"][weekOfDay][period]["course"] != None):
            # print registered course details
            print(f"Another course is registered on {weekOfDay}'s period {period}")
            print(f"Course registered: {timetable['weekday'][weekOfDay][period]['course']}")
            # ask if want to overwrite
            overwrite = input("Do you want to overwrite it?: (Y/y)")
            if (overwrite not in ['Y', 'y']):
                print(f"{courseToRegister['course']} is not registered.")
                return False
    # prepare new data for timetable.json
    print(f"Registering {courseToRegister['course']}...")
    for i in range(len(courseToRegister["weekday"])):
        weekOfDay = day_ref_jap_en[courseToRegister["weekday"][i]]
        period = courseToRegister["period"][i]
        timetable["weekday"][weekOfDay][period]["course"] = courseToRegister["course"]
        timetable["weekday"][weekOfDay][period]["lecturer"] = courseToRegister["lecturer"]
        timetable["weekday"][weekOfDay][period]["id"] = courseToRegister["id"]
    # update timetable.json
    with open("data/timetable.json", "w") as jsonFile:
        json.dump(timetable, jsonFile)

    print(f"{courseToRegister['course']} registered!")
    return True

if __name__ == "__main__":
    search('brain')
