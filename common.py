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

def Update_Guna(conn):
    
    if (os.path.isfile('List.txt') & os.path.exists('List.txt')):
        # Open the existing DB connection 
        try:
            with open("List.txt", "r") as fd:
                list_1 = fd.readlines()
        except IOError:
            print("Error in opening Credentials.txt\n")
            return
    else:
        print("List.txt doen't exist\n")
        return
    
    if (len(list_1) == 0):
        print("No data in list.txt\n")
        return
    
    list_1 = map(lambda s: s.strip(), list_1)
    
    print list_1
    
    c = conn.cursor()
    
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    browser = webdriver.Firefox(firefox_profile=firefox_profile)
#    browser.get('https://www.mpanchang.com/astrology/kundali-matching/')

    # Read the boys details
    try:
        c.execute("select candidate.f_name, candidate.dob, candidate.bir_time, candidate.bir_place from candidate where id = '1'")
    except IntegrityError:
        print ("Unable to read boys data from database\n")
    
    boy_data = c.fetchone()
    
    boy_f_name = "He"
    if (boy_data[0] != None):
        boy_f_name = boy_data[0]
    boy_date_list = boy_data[1].split('-')
    boy_time_list = boy_data[2].split(':')
    boy_bir_place = boy_data[3]
    
    # Desired values range is 01 to 12
    boy_month = boy_date_list[1]
    
    # Desired values range is 1 to 31
    boy_date = "{0:1}".format(int(boy_date_list[0]))
    
    # Desired values range is 2018 to 1918
    boy_year = boy_date_list[2]
    
    # Desired values range is 0 to 59
    boy_sec = "{0:1}".format(int(boy_time_list[2]))
    
    # Desired values range is 0 to 59
    boy_min = "{0:1}".format(int(boy_time_list[1]))
    
    if (int(boy_time_list[0]) > 12):
        boy_hour = str(int(boy_time_list[0]) - 12)
        # Desired values range is 0 to 12
        boy_hour = "{0:1}".format(int(boy_hour))
        boy_AM_PM = '02'
    else:
        boy_hour = "{0:1}".format(int(boy_time_list[0]))
        boy_AM_PM = '01'
    
    for ID in list_1:
        browser.get('https://www.drikpanchang.com/jyotisha/horoscope-match/horoscope-match.html')
        dash_board_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="dpBoyData"]')))
        
        try:
            c.execute("select candidate.f_name, candidate.dob, candidate.bir_time, candidate.bir_place from candidate where id = ?", (ID,))
        except IntegrityError:
            print ("Unable to read girls database\n")
        
        candidate_data = c.fetchone()
        print candidate_data
        
        if ((candidate_data[1] == None) or (candidate_data[2] == None) or (candidate_data[3] == None)):
            print ("Unable to get %s candidate data properly\n") %(ID)
            continue
        #Male Details
        browser.find_element_by_xpath('//input[@id="kmb-name"]').send_keys(boy_f_name)
        
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-month"]'))
        input_fields.select_by_value(boy_month)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-day"]'))
        input_fields.select_by_value(boy_date)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-year"]'))
        input_fields.select_by_value(boy_year)
        
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-hr"]'))
        input_fields.select_by_value(boy_hour)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-min"]'))
        input_fields.select_by_value(boy_min)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-sec"]'))
        input_fields.select_by_value(boy_sec)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmb-ampm"]'))
        input_fields.select_by_value(boy_AM_PM)
        
        browser.find_element_by_xpath('//input[@id="kmb-city"]').send_keys(boy_bir_place)
       
        #female details
        f_name = "She"
        if (candidate_data[0] != None):
            f_name = candidate_data[0]
        date_list = candidate_data[1].split('-')
        time_list = candidate_data[2].split(':')
        bir_place = candidate_data[3]
        
        # Desired values range is 01 to 12
        month = date_list[1]
        
        # Desired values range is 1 to 31
        date = "{0:1}".format(int(date_list[0]))
        
        # Desired values range is 2018 to 1918
        year = date_list[2]
        
        # Desired values range is 0 to 59
        sec = "{0:1}".format(int(time_list[2]))
        
        # Desired values range is 0 to 59
        min = "{0:1}".format(int(time_list[1]))
        
        if (int(time_list[0]) > 12):
            hour = str(int(time_list[0]) - 12)
            # Desired values range is 0 to 12
            hour = "{0:1}".format(int(hour))
            AM_PM = '02'
        else:
            hour = "{0:1}".format(int(time_list[0]))
            AM_PM = '01'
        
        print ("Entering following detials for girl\n")
        print ("\nName: %s") %(f_name)
        
        print ("\nMonth: %s") %(month)
        print ("\nDate: %s") %(date)
        print ("\nYear: %s") %(year)
        
        print ("\nHour: %s") %(hour)
        print ("\nMin: %s") %(min)
        print ("\nSec: %s") %(sec)
        print ("\nZone: %s") %(AM_PM)
        
        browser.find_element_by_xpath('//input[@id="kmg-name"]').send_keys(f_name)
        
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-month"]'))
        input_fields.select_by_value(month)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-day"]'))
        input_fields.select_by_value(date)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-year"]'))
        input_fields.select_by_value(year)
        
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-hr"]'))
        input_fields.select_by_value(hour)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-min"]'))
        input_fields.select_by_value(min)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-sec"]'))
        input_fields.select_by_value(sec)
        input_fields = Select(browser.find_element_by_xpath('//select[@id="kmg-ampm"]'))
        input_fields.select_by_value(AM_PM)
        
        browser.find_element_by_xpath('//input[@id="kmg-city"]').send_keys(bir_place)
        
        raw_input("Press Enter to continue...")
        
#        browser.find_element_by_xpath('//input[@id="dpSubmitDiv"]').click()
        
        final_result = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//th[contains(text(),"Total Guna Milan =")]')))
        
        guna_temp = re.findall("[\d.]+(?= ?out)",final_result.text)[0]
        
        print guna_temp
        
        guna = float(guna_temp)
        
        print "\nCalculated guna are %f" %(guna)
        
        try:
            c.execute("update candidate set guna = ? where id = ?", (guna, ID))
        except IntegrityError:
            print ("Unable to update guna in database\n")
        
        conn.commit()
        
        