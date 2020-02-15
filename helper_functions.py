#! python 3
#! utf-8

def login(browser, username, password):
    # get DOM elements
    usernameInput = browser.find_element_by_id('username')
    passwordInput = browser.find_element_by_id('password')
    loginButton = browser.find_element_by_id('loginbtn')
    # input
    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    loginButton.click()
