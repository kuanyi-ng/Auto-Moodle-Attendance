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
            if len(param[1:]) > 1:
                
                for course in param[1:]: 
                    content = search(course)
                    print(f"Search : {course}")
                    print(content+'\n')

                    option = input("Enter -1 if your course is not here!\nChoose one of the courses :")
                    if(option == -1):
                            retry = input("Search : ")
                            content = search(retry)

                            for i in range( len(content) ):
                                print(content[i])

                        else : 
                            # Maybe register into courses' csv
                            pass 

            else:
                content = search(param[1])

                # Receive possible search results
                if len(content) > 1:
                    print(content)
                    option = input("Enter -1 if your course is not here!\nChoose one of the courses :")

                    if(option == -1):
                        retry = input("Search : ")
                        content = search(retry)

                        for i in range( len(content) ):
                            print(content[i])

                    else : 
                        # Maybe register into courses' csv
                        pass 
        else:
            print("That feature is currently not available.\nPlease try it again.")
