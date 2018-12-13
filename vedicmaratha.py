# import os

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

from datetime import datetime

import urllib

# import time
# from _socket import timeout
# from pstats import browser

file_name = "VedicMaratha.db"
db_schema = '''CREATE TABLE IF NOT EXISTS candidate (
                    id text PRIMARY KEY,
                    l_name text,
                    cast text,
                    height real,
                    reg_date text,
                    edu text,
                    prof text,
                    income int,
                    dob text,
                    time text,
                    place text,
                    rashi text,
                    nak text)'''

def CreateNewDB():
    print ("Creating New DB\n")
    try:
        conn = sqlite3.connect("VedicMaratha.db")
    except Error as e:
        print(e)
    else:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS candidate (
                    id text PRIMARY KEY,
                    l_name text,
                    cast text,
                    height real,
                    reg_date text,
                    edu text,
                    prof text,
                    income int,
                    dob text,
                    time text,
                    place text,
                    rashi text,
                    nak text)''')
        return conn
#    finally:
#        conn.close()

def GetProfielPic(browser, xpath, candidate_id):
    try:
        cand_img = browser.find_element_by_xpath(xpath).get_attribute("src")
    except NoSuchElementException:
        print ("Unable to get profile pic\n")
        pass
    else:
        file_name = "snaps\\vedicmaratha\\" + candidate_id + '.jpeg'
#            print cand_img
        urllib.urlretrieve(cand_img, file_name)

def GetLastName(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text.encode('ascii','ignore')
    str2 = re.findall('(?<=\().+(?=\))', str1)[0].title()
    return str2.title()
    
def GetCast(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        return str1.title()
    else:
        return None
    
def GetHeight(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        str2 = re.findall('(?= )?\d', str1)[0]
        str3 = re.findall('(?= )?\d', str1)[1]
    
        return float(str2 +'.'+ str3)
    else:
        return None
    
def GetRegDate(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (str1 != '--'):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        str1 = str1.replace('-','/')
        return str1
    else:
        return None
        
    
def GetEdu(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore').title()
        return str1
    else:
        return None

def GetProf(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore').title()
        return str1
    else:
        return None
    
def GetInc(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        if (str1 == 'Monthly' or str1 == 'Yearly'):
            return None
        else:
            str1 = str1.replace('Monthly', '')
            str1 = str1.replace(' Yearly', '')
            str1 = str1.replace('Rs.', '')
            str1 = str1.replace(',', '')
            try:
                income = int(str1)
            except ValueError:
                print "Unable to conver %s into integer\n" %(str1)
                pass
                return None
            else:
                return income
    else:
        return None
    
def GetDOB(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (str1 != '--'):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        str1 = str1.replace('-','/')
    else:
        return None
    
def GetTime(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        time_lst = str1.split('-')
        try: 
            if (time_lst[0].isdigit() and time_lst[1].isdigit() and time_lst[-1] in ('AM', 'PM')):
    #             hr = int(re.findall('\d\d(?=-)', str1)[0])
    #             mins = int(re.findall('\d\d(?=-)', str1)[1])
                
                hr = int(time_lst[0])
                mins = int(time_lst[1])
                
                if (time_lst[-1] == 'PM'):
                    hr = hr + 12
                return "{:02}:{:02}".format(hr, mins)
            else:
                return None
        except IndexError:
            pass
            return None
    else:
        return None
    
def GetPlace(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore').title()
        return str1
    else:
        return None
    
def GetRashi(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.replace('Rashi / Nakshatra / Charan / Nadi / Gan:  ','')
        token = str1.split(',')
        if (token[0] != ' '):
            return None
        else:
            return token[0]
    else:
        return None
    
def GetNak(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.replace('Rashi / Nakshatra / Charan / Nadi / Gan:  ','')
        token = str1.split(',')
        if (token[1] != ' '):
            return None
        else:
            return token[1]
    else:
        return None
    
    
def StoreCandidateData(browser, c, candidate_id):
    
    l_name = None 
    cast = None
    height = None
    reg_date = None
    edu = None
    prof = None
    income = None
    dob = None
    time = None
    place = None
    rashi = None
    nak = None
    
    try:
        
        #Wait for login box to load
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="profile"]')))
#         time.sleep(3)
        GetProfielPic(browser, '//img[contains(@src, "photoprocess.php")]', candidate_id)
        l_name = GetLastName(browser, '(//td)[29]')
        cast  = GetCast(browser, '(//td[@class="data"])[6]')
        height  = GetHeight(browser, '(//td[@class="data"])[8]')
        reg_date = GetRegDate(browser, '(//td[@class="data"])[28]')
        edu = GetEdu(browser, '(//td[@class="data"])[30]')
        prof = GetProf(browser, '(//td[@class="data"])[32]')
        income = GetInc(browser, '(//td[@class="data"])[36]')
        dob = GetDOB(browser, '(//td[@class="data"])[2]')
        time = GetTime(browser, '(//td[@class="data"])[38]')
        place = GetPlace(browser, '(//td[@class="data"])[42]')
        rashi = GetRashi(browser, '(//td[@class="data"])[45]')
        nak = GetNak(browser, '(//td[@class="data"])[45]')
        
        ProfLink = browser.current_url
        now = datetime.now()
        ProfCreatTime = now.strftime("%d/%m/%Y")
        
        complete_det = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(candidate_id, l_name, cast, height, reg_date, edu, prof, income, dob, time, place, rashi, nak)
        
        print "%s\n" %(complete_det)
        
        try:
            c.execute("insert into PrimData (ProfId, LName, Height, Edu, Prof, Income) values (?, ?, ?, ?, ?, ?)", (candidate_id, l_name, height, edu, prof, income))
            
            c.execute("insert into CastData (ProfId, SCast) values (?, ?)", (candidate_id, cast))
            
            c.execute("insert into BirData (ProfId, BTime, BDate, MSign, Naksh) values (?, ?, ?, ?, ?)", (candidate_id, time, dob, rashi, nak))
            
            c.execute("insert into BirLocData (ProfId, City) values (?, ?)", (candidate_id, place))
            
            c.execute("insert into Metdata (ProfId, ProfRef, ProfLink, ProfCreatTime) values (?, ?, ?, ?)", (candidate_id, "Vedic Maratha", ProfLink, ProfCreatTime))

        except IntegrityError:
            print ("Unable to update the database\n")
            
    except NoSuchElementException as e:
        print ("StoreCandidateData : Unable to save the details because no such element\n")
        print e

    except TimeoutException:
        print ("StoreCandidateData : Unable to load the profile\n")


def found_window(window_title):

    def predicate(driver):
        for handle in driver.window_handles:
            try: driver.switch_to_window(handle)
            except NoSuchWindowException:
                    return False
            else:
                    if (driver.title == window_title):
                        return True  # found window
                    else:
                        continue

    return predicate


def CollectTenCandidatesData(browser, c):
    try:
        # We are now on new page of the candidates
        curr_candidate_xpath = "//a[contains(@href, 'profile_by_public')]"
        candidate_id_array = browser.find_elements_by_xpath(curr_candidate_xpath)
        
        for candidate_id in candidate_id_array:
            cand_id = candidate_id.text.strip().encode('ascii','ignore')
#             print "Value of cand id is %s" %(cand_id)
#             temp_var = (cand_id,)
            c.execute("select exists (select PrimData.ProfId from PrimData where PrimData.ProfId = ?)", (cand_id,))
            if (c.fetchone() == (0,)):
                #New candiate data found save it                
                main_window = browser.current_window_handle
                
                candidate_id.click()
#                 browser.implicitly_wait(30) 
#                 time.sleep(3)               
#                 print ("Number of windows opened  %d\n ") %(len(browser.window_handles))

                WebDriverWait(browser, 10, 2).until(found_window('Member Profile'))
                StoreCandidateData(browser, c, cand_id)
                browser.close()
                browser.switch_to_window(main_window)
                

                #switch to new window
#                browser.switch_to_window(browser.window_handles[1])
#                browser.switch_to_window('')
#                print ("Title of window  %s\n ") %browser.title

#                 
#                 for handle in browser.window_handles:
#                     if (main_window != handle):
#                         browser.switch_to_window(handle)
#                         print ("Switched to new window %s\n ") %browser.title
#                         StoreCandidateData(browser, c, cand_id)
#                         browser.close()
#                         browser.switch_to_window(main_window)
                
            else:
                print "%s is already in DB\n" %(cand_id)
    except NoSuchElementException as e:
        print ("CollectTenCandidatesData : Unable to find some elements\n")
        print (e)


def NagivateToDashBoard(login_ID, login_pass, login_page, browser):
    
    browser.get(login_page)
    try:
        #Wait for login box to load
        login_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//table[@id="example"]')))
        
        #Select Number of entries
        login_element = Select(browser.find_element_by_xpath('//select[@name="example_length"]'))
        login_element.select_by_value('100')
        browser.implicitly_wait(5)
        
        #Wait for Dashboard to load
#        dash_board_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="cPageData"]')))
        
    except NoSuchElementException:
        print ("Unable to navigate to pavitra vivah dash board\n")

    except TimeoutException:
        print ("Unable to use dash board due to time out\n")


def GetPageNum():
    print ("GetPageNum\n")
    
def GoNextPage(browser):
    browser.find_element_by_xpath('//a[@class="paginate_button next"]').click()
    
def ScrapLoadedPages(browser, conn):
    #Rotate through all the search result pages
    c = conn.cursor()
    
    while (True):
        try:
            
            #Wait for the results to load
            WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="dataTable no-footer"]')))
            
            CollectTenCandidatesData(browser, c)
            
            print ("Moving on to Next page\n")
            GoNextPage(browser)
                
        except NoSuchElementException as e:
            print ("Seems like we are on last page, saving changes to database\n")
            print e
            break
    
#     conn.commit()
#     c.close()

def CollectAllQuickSearch(browser, conn):
    
    ScrapLoadedPages(browser, conn)
