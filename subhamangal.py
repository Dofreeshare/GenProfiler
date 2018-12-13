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

script = """
    var text = '';

    var childNodes = arguments[0].childNodes; // child nodes includes Element and Text Node

    childNodes.forEach(function(it, index)
    {
      if(it.nodeName.toUpperCase() === 'DIV') 
      { // iterate until Element Node: hr
        text = childNodes[index+1].textContent; 
        // get the text content of next Child Node of Element Node: hr
      }
    });
    return text;
"""

def CreateNewDB():
    print ("Creating New DB\n")
    try:
        conn = sqlite3.connect("Shunbhamangal.db")
    except Error as e:
        print(e)
    else:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS candidate (
                    id text PRIMARY KEY,
                    l_name text,
                    height real,
                    edu text,
                    age int,
                    income int,
                    ocupation text)''')
        return conn
#    finally:
#        conn.close()

def StoreCandidateData(browser, c, curr_candidate_index, candidate_id, surname):
    
    l_name = None
    height = None
    edu = None
    age = None
    income_yearly = None
    profession = None
    
    try:
        
        l_name = surname.encode('ascii','ignore').title()
#        l_name = l_name.Title()
#        print l_name
        
        try:
            cand_img = browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="items"]/div['+str(curr_candidate_index)+']/div/div/div/a').get_attribute("href")
        except NoSuchElementException as e:
            print ("Unable to get profile pic\n")
        else:
#        if (cand_img):
            file_name = "snaps\\" + candidate_id + '.jpeg'
#            print cand_img
            urllib.urlretrieve(cand_img, file_name)
        
        can_det_element = browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="items"]/div['+str(curr_candidate_index)+']/div/div[2]')
        
#        raw_string_1 = browser.execute_script('return arguments[0].childNodes[1].textContent;', can_det_element).strip()
#        raw_string_2 = browser.execute_script('return arguments[0].childNodes[2].textContent;', can_det_element).strip()
#        raw_string_3 = browser.execute_script('return arguments[0].childNodes[3].textContent;', can_det_element).strip()
#        raw_string_4 = browser.execute_script('return arguments[0].childNodes[4].textContent;', can_det_element).strip()
#        raw_string_5 = browser.execute_script('return arguments[0].childNodes[5].textContent;', can_det_element).strip()
#        raw_string_6 = browser.execute_script('return arguments[0].childNodes[6].textContent;', can_det_element).strip()
#        raw_string_7 = browser.execute_script('return arguments[0].childNodes[7].textContent;', can_det_element).strip()
#        raw_string_8 = browser.execute_script('return arguments[0].childNodes[8].textContent;', can_det_element).strip()
#        raw_string_9 = browser.execute_script('return arguments[0].childNodes[9].textContent;', can_det_element).strip()
#        raw_string_10 = browser.execute_script('return arguments[0].childNodes[10].textContent;', can_det_element).strip()
#        raw_string_11 = browser.execute_script('return arguments[0].childNodes[11].textContent;', can_det_element).strip()
#        raw_string_12 = browser.execute_script('return arguments[0].childNodes[12].textContent;', can_det_element).strip()
#        raw_string_13 = browser.execute_script('return arguments[0].childNodes[13].textContent;', can_det_element).strip()
#        raw_string_14 = browser.execute_script('return arguments[0].childNodes[14].textContent;', can_det_element).strip()
#        raw_string_15 = browser.execute_script('return arguments[0].childNodes[15].textContent;', can_det_element).strip()
#        raw_string_16 = browser.execute_script('return arguments[0].childNodes[16].textContent;', can_det_element).strip()
#        raw_string_17 = browser.execute_script('return arguments[0].childNodes[17].textContent;', can_det_element).strip()
#        raw_string_18 = browser.execute_script('return arguments[0].childNodes[18].textContent;', can_det_element).strip()
#        
#        print "Value at index 01 %s " %(raw_string_1)
#        print "Value at index 02 %s " %(raw_string_2)
#        print "Value at index 03 %s " %(raw_string_3)
#        print "Value at index 04 %s " %(raw_string_4)
#        print "Value at index 05 %s " %(raw_string_5)
#        print "Value at index 06 %s " %(raw_string_6)
#        print "Value at index 07 %s " %(raw_string_7)
#        print "Value at index 08 %s " %(raw_string_8)
#        print "Value at index 09 %s " %(raw_string_9)
#        print "Value at index 10 %s " %(raw_string_10)
#        print "Value at index 11 %s " %(raw_string_11)
#        print "Value at index 12 %s " %(raw_string_12)
#        print "Value at index 13 %s " %(raw_string_13)
#        print "Value at index 14 %s " %(raw_string_14)
#        print "Value at index 15 %s " %(raw_string_15)
#        print "Value at index 16 %s " %(raw_string_16)
#        print "Value at index 17 %s " %(raw_string_17)
#        print "Value at index 18 %s " %(raw_string_18)
        
#        print "\n\n\n\n\n\n\n\n"
        
        # Edu
        raw_string = browser.execute_script('return arguments[0].childNodes[2].textContent;', can_det_element).strip()
        raw_string = raw_string.encode('ascii','ignore').strip().title()
        print "Education Details is %s" %(raw_string)
        edu = raw_string
        
        # Height
        raw_string = browser.execute_script('return arguments[0].childNodes[6].textContent;', can_det_element).strip()
        raw_string = raw_string.encode('ascii','ignore').strip()
        print "Value of the salary is %s" %(raw_string)
        height = float(raw_string)

        # Age
        raw_string = browser.execute_script('return arguments[0].childNodes[10].textContent;', can_det_element).strip()
        raw_string = raw_string.encode('ascii','ignore').strip().title()
        print "Age of candiate is %s" %(raw_string)
        age = int(raw_string)
        
        # Income
        raw_string = browser.execute_script('return arguments[0].childNodes[14].textContent;', can_det_element).strip()
        raw_string = raw_string.encode('ascii','ignore').strip().title()
        print "Income is %s" %(raw_string)
        income_yearly = int(raw_string)
        
        # Profession
        raw_string = browser.execute_script('return arguments[0].childNodes[18].textContent;', can_det_element).strip()
        raw_string = raw_string.encode('ascii','ignore').strip().title()
        print "Profession is %s" %(raw_string)
        profession = raw_string
        
        try:
            c.execute("insert into candidate (id, l_name, height, edu, age, income, ocupation) values (?, ?, ?, ?, ?, ?, ?)", (candidate_id, l_name, height, edu, age, income_yearly, profession))

        except IntegrityError:
            print ("Unable to update the database\n")
            
    except NoSuchElementException as e:
        print ("StoreCandidateData : Unable to save the details because no such element\n")
        print e

    except TimeoutException:
        print ("StoreCandidateData : Unable to load the profile\n")

def NagivateToDashBoard(login_ID, login_pass, login_page):
    
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    browser = webdriver.Firefox(firefox_profile=firefox_profile, executable_path="D:\Portables\geckodriver")
    browser.get(login_page)
    try:
        #Wait for login box to load
        login_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="container"]')))
        
        #Select Height
        login_element = Select(browser.find_element_by_xpath('//select[@name="height"]'))
        login_element.select_by_value('N/A')
        browser.implicitly_wait(5)
        
        #Select Native
        login_element = Select(browser.find_element_by_xpath('//select[@name="native"]'))
        login_element.select_by_value('N/A')
        browser.implicitly_wait(5)
        
        #Select Edu
        login_element = Select(browser.find_element_by_xpath('//select[@name="education"]'))
        login_element.select_by_value('N/A')
        browser.implicitly_wait(5)
        
        #Select Marriage
        login_element = Select(browser.find_element_by_xpath('//select[@name="marriageType"]'))
        login_element.select_by_value('Single')
        browser.implicitly_wait(5)
        
        #Select Gender
        login_element = Select(browser.find_element_by_xpath('//select[@name="sex"]'))
        login_element.select_by_value('Female')
        browser.implicitly_wait(5)
        
        #Wait for Dashboard to load
#        dash_board_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="cPageData"]')))
        return browser
        
    except NoSuchElementException:
        print ("Unable to navigate to pavitra vivah dash board\n")
        return None
    except TimeoutException:
        print ("Unable to use dash board due to time out\n")
        return None

def CollectTenCandidatesData(browser, c):
    curr_candidate_index = 1
    while(True):
        try:
            # We are now on new page of the candidates
            curr_candidate_xpath = '//div[@id="candidateBriefInformation"]/div[@class="items"]/div['+str(curr_candidate_index)+']/header'
            title_str = browser.find_element_by_xpath(curr_candidate_xpath).text
            title_str = title_str.strip()
            candidate_id = title_str.split(" ")[0]
            surname = title_str.split(" ")[-1]
#            print "Found this as ID and surname %s %s" %(candidate_id, surname)
            temp_var = (candidate_id,)
            c.execute("select exists (select candidate.id from candidate where candidate.id = ?)", (temp_var))
            if (c.fetchone() == (0,)):
                #New candiate data found save it
                print "Saving the data of %s" %(candidate_id)
                StoreCandidateData(browser, c, curr_candidate_index, candidate_id, surname)
            else:
                print "%s is already in DB\n" %(candidate_id)
                
            curr_candidate_index = curr_candidate_index + 1
        except NoSuchElementException as e:
            print ("CollectTenCandidatesData : Unable to find some elements\n")
            print (e)
            break
    
def ScrapLoadedPages(browser, conn):
    #Rotate through all the search result pages
    c = conn.cursor()
    
    while(True):
        try:
            reload_attempt = 0
            next_attempt = 0
            #Wait for the results to load
            browser.implicitly_wait(10)
            dash_board_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="candidateBriefInformation"]/div[@class="items"]')))
            
            current_page = browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="pager"]/ul/li[@class="page selected"]').text
            print("Collecting Data on page " + current_page)
            
            CollectTenCandidatesData(browser, c)
            conn.commit()
            
            print ("Moving on to Next page\n")
            
            while (True):
#                browser.execute_script("document.getElementById('ctl00_ContentPlaceHolder1_lbtnNext1').click()")
                browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="pager"]/ul/li[@class="next"]/a').click()
                browser.implicitly_wait(10)
#                time.sleep(10)
#                WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//span[@id="ctl00_ContentPlaceHolder1_dlsearch"]')))
                next_page = browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="pager"]/ul/li[@class="page selected"]').text
                if (current_page == next_page):
                    if (next_attempt < 5):
                        print ("Seems like unable to click the next button\n")
                        next_attempt = next_attempt + 1
                        browser.implicitly_wait(5)
                        continue
                    else:
                        print ("Unable to click the next after so many attempts trying refresh\n")
                        browser.refresh()
                        next_attempt = 0
                        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="candidateBriefInformation"]/div[@class="items"]')))
                        continue
                else:
                    break
#            browser.find_element_by_xpath('//a[@id="ctl00_ContentPlaceHolder1_lbtnNext1"]').click()
        
        except NoSuchElementException as e:
            print ("Seems like we are on last page, saving changes to database\n")
            print e
            conn.commit()
            c.close()
            break
        except TimeoutException:
            #We try to reload the page and for particular amount of time and then press next
            reload_attempt = reload_attempt + 1
            if (reload_attempt == 3):
                print ("Skipping this page and moving forward\n")
                temp_elem = browser.find_element_by_xpath('//div[@id="candidateBriefInformation"]/div[@class="pager"]/ul/li[@class="next"]')
                temp_elem.click()
            else:
                print ("Refreshing the current Page\n")
                browser.refresh()
            #Continue to the while loop
            continue
            
    
    conn.commit()
    c.close()

def CollectAllQuickSearch(browser, conn):
    
    ScrapLoadedPages(browser, conn)
