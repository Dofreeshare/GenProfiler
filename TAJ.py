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

import os
from pandas._libs.testing import isnull

# import time
# from _socket import timeout
# from pstats import browser

age_from = "25"
age_to = "29"

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
        if (cand_img != 'https://www.tumchaaamchajamla.com/images/Default_Profile.png'):
            file_name = "snaps\\tumchaaamchajamla\\" + candidate_id + '.jpeg'
            urllib.urlretrieve(cand_img, file_name)
#         else:
#             print("Looks like default Pic\n")

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
        return float(re.findall("(\d+.?\d+)(?= cms)", str1)[0])
    else:
        return None
    
def GetWeight(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        return float(re.findall("(\d+.?\d+ ?)(?=Kg)", str1)[0])
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
        str1 = str1.replace('"', '')
        str1 = str1.replace("'", "")
        str1 = str1.encode('ascii','ignore').title()
        return str1
    else:
        return None

def GetProf(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.replace('"', '')
        str1 = str1.replace("'", "")
        str1 = str1.encode('ascii','ignore').title()
        return str1
    else:
        return None
    
def GetInc(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    income = None
    Currency = None
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        if (-1 != str1.find('INR')):
            Currency = 'INR';
            str1 = str1.replace('INR - ', '')
        elif (-1 != str1.find('USD')):
            Currency = 'USD';
            str1 = str1.replace('USD - ', '')
        elif (-1 != str1.find('Pound')):
            Currency = 'PND';
            str1 = str1.replace('Pound - ', '')
            
        str1 = str1.replace(',', '')
        income = str1
    return income, Currency
    
def GetDOB(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        str1 = str1.replace(' - ','-')
        return str1
    else:
        return None
    
def GetTime(browser, xpath):
    str1 = browser.find_element_by_xpath(xpath).text
    if (not(str1 == None or str1 == '')):
        str1 = str1.strip()
        str1 = str1.encode('ascii','ignore')
        
        hour = int(re.findall("\d+", str1)[0])
        minutes = int(re.findall("\d+", str1)[1])
        sec = 0
        bir_time = "{:0>2}:{:0>2}:{:0>2}".format(hour,minutes,sec)   
        return bir_time
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
    
    cast = None
    subcast = None
    height = None
    edu = None
    income = None
    Currency = None
    prof = None
    
    dob = None
    time = None
    place = None
    
    try:
        
#         time.sleep(3)
        GetProfielPic(browser, '//img[@id="imgDatingProfileView_PhotoMain"]', candidate_id)
    
        cast  = GetCast(browser, '//div[contains(text(), "Caste")]/following-sibling::div')
        subcast = GetCast(browser, '//div[contains(text(), "Sub Caste")]/following-sibling::div')
        
        height  = GetHeight(browser, '//div[contains(text(), "Height")]/following-sibling::div')
        weight = GetWeight(browser, '//div[contains(text(), "Weight")]/following-sibling::div')
        
        edu = GetEdu(browser, '//div[contains(text(), "Education Details")]/following-sibling::div')
        
        (income, Currency) = GetInc(browser, '//div[contains(text(), "Annual Income")]/following-sibling::div')        
        
        prof = GetProf(browser, '//div[contains(text(), "Profession")]/following-sibling::div')
        
        dob = GetDOB(browser, '//div[contains(text(), "Birth Date")]/following-sibling::div') # Birth Date
        time = GetTime(browser, '//div[contains(text(), "Birth Time")]/following-sibling::div') # Birth Time
        place = GetPlace(browser, '//div[contains(text(), "Birth Place")]/following-sibling::div') # Birth Place
        
        ProfLink = browser.current_url
        now = datetime.now()
        ProfCreatTime = now.strftime("%d/%m/%Y")
        
        complete_det = "{}|{}|{}|{} cm|{} Kg|{}|{} {}|{}|{}|{}".format(candidate_id, cast, subcast, height, weight, edu, income, Currency, prof, dob, time, place)
        
        print "%s\n" %(complete_det)
        
        try:
            db_string = "UPDATE PrimData SET Height = {0}, Weight = {1}, Edu = {2}, Prof = {3}, Income = {4}, IncCur = {5} where ProfId = {6}".format(
                          (height if (height != None) else 'null'),
                          (weight if (weight != None) else 'null'),
                          (("'{}'".format(edu)) if (edu != None) else 'null'),
                          (("'{}'".format(prof)) if (prof != None) else 'null'),
                          (("'{}'".format(income)) if (income != None) else 'null'),
                          (("'{}'".format(Currency)) if (Currency != None) else 'null'),
                          (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'))
#             print db_string
#             print "\n\n"
            c.execute(db_string)
            
            c.execute("select exists (select CastData.ProfId from CastData where CastData.ProfId = ?)", (candidate_id,))
            if (c.fetchone() == (1,)):
                db_string = "UPDATE CastData SET MCast = {1}, SCast = {2} where ProfId = {0}".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(cast)) if (cast != None) else 'null'), 
                            (("'{}'".format(subcast)) if (subcast != None) else 'null'))
            else:
                db_string = "insert into CastData (ProfId, MCast, SCast) values ({0}, {1}, {2})".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(cast)) if (cast != None) else 'null'), 
                            (("'{}'".format(subcast)) if (subcast != None) else 'null'))
#             print db_string
#             print "\n\n"
            c.execute(db_string)
            
            c.execute("select exists (select BirData.ProfId from BirData where BirData.ProfId = ?)", (candidate_id,))
            if (c.fetchone() == (1,)):
                db_string = "UPDATE BirData SET BTime = {1}, BDate = {2} where ProfId = {0}".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(time)) if (time != None) else 'null'), 
                            (("'{}'".format(dob)) if (dob != None) else 'null'))
            else:
                db_string = "insert into BirData (ProfId, BTime, BDate) values ({0}, {1}, {2})".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(time)) if (time != None) else 'null'), 
                            (("'{}'".format(dob)) if (dob != None) else 'null'))
#             print db_string
#             print "\n\n"
            c.execute(db_string)
            
            c.execute("select exists (select BirLocData.ProfId from BirLocData where BirLocData.ProfId = ?)", (candidate_id,))
            if (c.fetchone() == (1,)):
                db_string = "UPDATE BirLocData SET City = {1} where ProfId = {0}".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(place)) if (place != None) else 'null'))
            else:
                db_string = "insert into BirLocData (ProfId, City) values ({0}, {1})".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(place)) if (place != None) else 'null'))
#             print db_string
#             print "\n\n"
            c.execute(db_string)
            
            c.execute("select exists (select Metdata.ProfId from Metdata where Metdata.ProfId = ?)", (candidate_id,))
            if (c.fetchone() == (1,)):
                db_string = "UPDATE Metdata SET ProfLink = {1}, ProfCreatTime = {2} where ProfId = {0}".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(ProfLink)) if (ProfLink != None) else 'null'), 
                            (("'{}'".format(ProfCreatTime)) if (ProfCreatTime != None) else'null'))
            else:
                db_string = "insert into Metdata (ProfId, ProfLink, ProfCreatTime) values ({0}, {1}, {2})".format(
                            (("'{}'".format(candidate_id)) if (candidate_id != None) else 'null'), 
                            (("'{}'".format(ProfLink)) if (ProfLink != None) else 'null'), 
                            (("'{}'".format(ProfCreatTime)) if (ProfCreatTime != None) else'null'))
#             print db_string
#             print "\n\n"
            c.execute(db_string)
 
        except IntegrityError as e:
            print ("Unable to update the database\n")
            print e
            
    except NoSuchElementException as e:
        print ("StoreCandidateData : Unable to save the details because no such element\n")
        print e

    except TimeoutException:
        print ("StoreCandidateData : Unable to load the profile\n")


def found_window(profile_num):

    def predicate(driver):
        for handle in driver.window_handles[1:]:
            try: 
                driver.switch_to_window(handle)
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH , '//div[@class="PageMidBG"]')))
                str1 = driver.find_element_by_xpath('//span[contains(text(), "Profile ")]/following-sibling::span').text
                str1 = str1.strip()
#                 print str1
                if (profile_num == str1):
                    return True  # found window
                else:
                    continue
                    
            except NoSuchWindowException:
                print ("Window not listed hence unable to switch to window\n")
                return False
            except NoSuchElementException as e:
                print ("Unable to switch because unable to find elements below mentioned\n")
                print (e)
                pass
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
        #Input the user name
        login_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtUsername')))
        login_element.send_keys(login_ID)
        login_element.submit()
        
        #Input password
        login_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#txtPassword')))
        login_element.send_keys(login_pass)
        login_element.submit()
        
#        pop_up_element = browser.find_element_by_xpath('//a[@class="popup-modal-dismiss"]')
        pop_up_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//a[@class="popup-modal-dismiss"]')))
        pop_up_element.click()
        
        #Wait for Dashboard to load
        WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="MenuIconLinks_Div"]')))
        
    except NoSuchElementException:
        print ("Unable to find out login forms\n")
        return None
    except TimeoutException:
        print ("Timeout happened\n")
        return None


def GetPageNum():
    print ("GetPageNum\n")
    
def GoNextPage(browser):
    browser.find_element_by_xpath('//a[@class="paginate_button next"]').click()
    
def CollectDetailedInformation(browser, conn):
    
    if (os.path.isfile('List.txt') & os.path.exists('List.txt')):
        # Open the existing DB connection 
        try:
            with open("List.txt", "r") as fd:
                list_of_cand = fd.readlines()
        except IOError:
            print("Error in opening Credentials.txt\n")
    else:
        print("List.txt doen't exist\n")
        
    c = conn.cursor()
    try:
        # Scraping the Search results
        main_window = browser.current_window_handle
        
        #Wait for Dashboard to load
        dash_board_element = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH, '//div[@onclick="CheckMyProfileStatus(1);"]')))
        dash_board_element.click()
        
        #Quick search
        qck_srch_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH , '//div[@id="divDatingQuickSearch_MainSearchBlock"]')))
        
        for ID in list_of_cand:
            qck_srch_element = browser.find_element_by_xpath('//input[@id="txtDatingQuickSearch_SearchByKeyword"]')
            qck_srch_element.send_keys(ID)
            
            qck_srch_element = browser.find_element_by_xpath('//input[@class="DatingCSS_SearchButton"]')
            qck_srch_element.click()
            
            #Wait for the results to load
            WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH , '//div[@class="ResultList"]')))
    
            candidate_link = browser.find_element_by_xpath('//div[@class="ResultList"]/div[1]//a[@class="LinkBold"]')
            candidate_link.click()
            
            #switch to new window
#             browser.switch_to_window(browser.window_handles[1])
            WebDriverWait(browser, 10, 2).until(found_window("ID: " + ID.strip()))
            
#             candidate_page = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH , '//div[@class="PageMidBG"]')))
            
            StoreCandidateData(browser, c, ID.strip())
#             print "trying to close window\n"
            browser.close()
#             print "Moving to next window\n"
            browser.switch_to_window(main_window)
#             browser.implicitly_wait(1)
            qck_srch_element = browser.find_element_by_xpath('//input[@id="txtDatingQuickSearch_SearchByKeyword"]')
            qck_srch_element.clear()
        
    except NoSuchElementException:
        print ("Unable to find out login forms\n")
    except TimeoutException:
        print ("Timeout happened\n")
    except IndexError:
        pass
    
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

def QuickSearchCollectList(browser, c, curr_candidate_index):
    
    while(True):
        try:        
            curr_candidate_xpath = '(//div[@class="ResultBlock"]/div/div[@class="Text"][1])['+str(curr_candidate_index)+']'
            
            title = browser.find_element_by_xpath(curr_candidate_xpath).text
            title = title.strip()
            title = title.encode('ascii','ignore')
            title = title.replace('(', '')
            title = title.replace(')', '')
            title_list = title.split(' ')
            cand_id = title_list[-1]
            
            print cand_id
            
            c.execute("select exists (select PrimData.ProfId from PrimData where PrimData.ProfId = ?)", (cand_id,))
            if (c.fetchone() == (0,)):
                #New candiate data found save it
                if (len(title_list) == 1):
                    l_name = None
                    f_name = None
                elif (len(title_list) == 2):
                    l_name = title_list[-2]
                    f_name = None
                elif (len(title_list) == 3):
                    l_name = title_list[-2]
                    f_name = title_list[-3]
            
                curr_candidate_xpath = '(//div[@class="ResultBlock"]/div/div[@class="Text"][2])['+str(curr_candidate_index)+']'
                address_str = browser.find_element_by_xpath(curr_candidate_xpath).text.strip().encode('ascii','ignore')
                
                address_tag = address_str.split('\n')
                
                try:
                
                    city_extract_new = address_tag[-1].split(',')
                    country = city_extract_new[-1].strip().capitalize()
                    state = None
                    city = None
                    if (len(city_extract_new) == 2):
                        state = city_extract_new[-2].strip().capitalize()
                        city = None
                    elif(len(city_extract_new) == 3):
                        state = city_extract_new[-2].strip().capitalize()
                        city = city_extract_new[-3].strip().capitalize()
                    
                except IndexError:
                    pass
                
                print "{}|{}|{}|{}|{}\n".format(cand_id, f_name, l_name, country, state, city)
                
                try:
                    c.execute("insert into PrimData (ProfId, FName, LName) values (?, ?, ?)", (cand_id, f_name, l_name))
                    
                    c.execute("insert into CurLocData (ProfId, Country, State, City) values (?, ?, ?, ?)", (cand_id, country, state, city))
                    
                    c.execute("insert into Metdata (ProfId, ProfRef) values (?, ?)", (cand_id, "TAJ"))
    
                except IntegrityError:
                    print ("Unable to update the database\n")
            
            curr_candidate_index = curr_candidate_index + 1
            
        except NoSuchElementException:
            print ("Collected Data of all 10 Candidates\n")
            pass
            break
        
    return curr_candidate_index

def CollectAllQuickSearch(browser, conn):
    
    c = conn.cursor()
    try:
        dash_board_element = browser.find_element_by_xpath('//div[@onclick="CheckMyProfileStatus(1);"]')
        dash_board_element.click()
        
        #Quick search
        qck_srch_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH , '//div[@id="divDatingQuickSearch_MainSearchBlock"]')))
        
        qck_srch_element = browser.find_element_by_xpath('//select[@id="selDatingQuickSearch_AgeFrom"]')
        select = Select(qck_srch_element)
        select.select_by_visible_text(age_from)
        
        qck_srch_element = browser.find_element_by_xpath('//select[@id="selDatingQuickSearch_AgeTo"]')
        select = Select(qck_srch_element)
        select.select_by_visible_text(age_to)
        
        qck_srch_element = browser.find_element_by_xpath('//select[@id="selDatingQuickSearch_Caste"]')
        select = Select(qck_srch_element)
        select.select_by_value("2")
        
        qck_srch_element = browser.find_element_by_xpath('//input[@class="DatingCSS_SearchButton"]')
        qck_srch_element.click()
        
        curr_candidate_index = 1
        while(True):
            #Wait for the results to load
            all_list = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH , '//div[@class="ResultList"]')))

            curr_candidate_index = QuickSearchCollectList(browser, c, curr_candidate_index)
            
#             curr_candidate_index = curr_candidate_index + 1
                
            print ("Clicking the for more Updates\n")
            temp_elem = browser.find_element_by_xpath('//div[@id="divMoreUpdates"]')
            temp_elem.click()
            browser.implicitly_wait(5)
            
    except NoSuchElementException:
        print ("Unable to find out login forms\n")
    except TimeoutException:
        print ("Timeout happened\n")
        
    finally:
#    browser.close()
        conn.commit()
        c.close()
