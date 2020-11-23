import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import random
import CustomConstants
from selenium.webdriver.common.keys import Keys
from HelperClasses import ConfigurationObject

from Logger import ActionLog

def LoginToFacebook(username, pw,driver):
    ActionLog("[LOGGING IN TO FACEBOOK] [USERNAME {}]".format(username))

    
    driver.get('http://Facebook.com')
    time.sleep(5)
    
    page_src  = driver.page_source
    email     = ""
    password  = ""
    submitbtn = ""
    if 'on your mind' in page_src or 'Add Picture' in page_src:
        ActionLog("[FACEBOOK ALREADY LOGIN]")
        return True
    else:
        
        try:
            email = driver.find_element_by_id('email')
            password = driver.find_element_by_id('pass')
            email.send_keys(username)
            time.sleep(5)
            password.send_keys(pw)
            time.sleep(5)

            submitbtn = driver.find_element_by_id('loginbutton')
            submitbtn.click()
            time.sleep(7)
            page_src = driver.page_source
            
        except:

            ActionLog("[LOGIN UNSUCCESSFUL] [LOGIN CREDENTIALS NOT PROCESSED]")
            ActionLog("Email Box: {}".format(str(email)))
            ActionLog("Password Box: {}".format(str(password)))
            ActionLog("Submit Button: {}".format(str(submitbtn)))
            return False
    
    ##### UNEXPECTED ERROR CHECK #####
    ##### UNEXPECTED ERROR CHECK #####
    ##### UNEXPECTED ERROR CHECK #####
    if 'on your mind' in page_src or 'Add Picture' in page_src:
        return True
    else:
        ActionLog("[LOGIN UNSUCCESSFUL] [UNEXPECTED ERROR, CHECK SCREENSHOT]")
        return False

def Account_Login(driver):

    is_logged_in   = False
    log_in_retries = 5
    
    while(log_in_retries >= 0):
        if (LoginToFacebook(ConfigurationObject.FB_USER, ConfigurationObject.FB_PASS,driver)):
            is_logged_in = True
            break
        log_in_retries -= 1
    
    if(is_logged_in == False):       
        ActionLog("[LOGIN ATTEMPT FAILED] [EXITING]")
        TakeScreenShot(driver,CustomConstants.GetScreenShotFailedAtLoginPrefix(FB_USER))
        return 0
    
    ActionLog("[LOGIN ATTEMPT SUCCESSFUL]")
    return 1
