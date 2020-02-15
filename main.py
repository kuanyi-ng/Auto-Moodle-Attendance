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
    task = sys.argv[1:2] # this decides what the program will do
    if len(task) == 0:
        print('Usage: python main.py <feature>.')
        print("""
            Features currently available:
            1. Automatic Attendance <attend>
            2. Search for a Subject <search>
        """)
    else:
        print(task)
        if (task[0] == 'attend'):
            attend()
        elif (task[0] == 'search'):
            search()
        else:
            print("That feature is currently not available.\nPlease try it again.")
