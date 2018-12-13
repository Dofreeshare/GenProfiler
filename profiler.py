import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *

import sqlite3
from sqlite3 import Error, IntegrityError

import re

import sys, getopt
import getpass

import urllib

import time

from subhamangal import *
from common import *

help_banner = """python profiler.py -[option]

-h : for this banner
-a : Program will request you for Username and Password
-t : Text file having user name and password in it
     Please make sure its name is Credentials.txt
-l : Level of the profile data collections
"""

login_ID = None
login_pass = None
login_page = None
age_from = "1989"
age_to = "1993"


def GetCredentialsFromFile():
    ID = None
    password = None
    page = None
    
    if (os.path.isfile('Credentials.txt') & os.path.exists('Credentials.txt')):
        # Open the existing DB connection 
        try:
            with open("Credentials.txt", "r") as fd:
                ID = fd.readline()
                password = fd.readline()
                page = fd.readline()
                
        except IOError:
            print("Error in opening Credentials.txt\n")
    else:
        print("Credentials.txt doen't exist\n")
    
    return ID, password, page

        
def kill_popup(browser):
    
    try:
         browser.find_element_by_xpath('//img[@alt="banner_popup_2"]/preceding::button[@data-dismiss="modal"]').click()
    except NoSuchElementException:
        print ("Seems like no popup to face\n")



        
def main(argv):
    
    global login_ID
    global login_pass
    global login_page
    
    try:
        opts, remaining = getopt.getopt(argv, "hatl:")
    except getopt.GetoptError:
        print (help_banner)
    
    if (len(opts) == 0):
        print (help_banner)
        sys.exit()
    else:
        for o,a in opts:
            if o in ('-h'):
                print (help_banner)
            if o in ('-a'):
                login_ID = raw_input("Username:")
                login_pass = getpass.getpass("Password for " + login_ID + ":")
                login_page = raw_input("Enter Login page:")
            if o in ('-t'):
                (login_ID, login_pass, login_page) = GetCredentialsFromFile()
            if o in ('-l'):
                profiler_level = int(a)
                print (a)
    
#    sys.exit()
    
    conn = CreateNewDB()
    
    #Collect the First Stage of data
    if (profiler_level == 1):
        print ("Collecting only primary info\n")
        browser = NagivateToDashBoard(login_ID, login_pass, login_page)
        CollectAllQuickSearch(browser, conn)
    elif(profiler_level == 2):
        print ("Updating the Guna\n")
        Update_Guna(conn)
    
if __name__ == '__main__':
    main(sys.argv[1:])
