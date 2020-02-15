#! python 3
#! utf-8

""" Variables """
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

def login(browser, username, password):
    # get DOM elements
    usernameInput = browser.find_element_by_id('username')
    passwordInput = browser.find_element_by_id('password')
    loginButton = browser.find_element_by_id('loginbtn')
    # input
    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    loginButton.click()
