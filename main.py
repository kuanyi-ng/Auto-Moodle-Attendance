#! python 3
#! utf-8

import getpass
import re
import requests
import sys

from bs4 import BeautifulSoup
from helper_functions import *

if __name__ == "__main__":
    # get argument from terminal
    param = sys.argv[1:] # this decides what the program will do
    if (len(param) == 0):
        print('Usage: python main.py <feature>.')
        print("""
            Features currently available:
            1. Automatic Attendance <attend>
            2. Automatic Attendance (Replacement Class) <attend replace>
            3. Search for a Subject <search>
        """)
    else:
        if (param[0] == 'attend'):
            if ('replace' in param[1:]):
                attend(replace=True)
            else:
                attend()
        elif (param[0] == 'search'):
            search()
        else:
            print("That feature is currently not available.\nPlease try it again.")
