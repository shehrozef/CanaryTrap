import time
import random
import CustomConstants
from selenium.webdriver.common.keys import Keys

from Logger import ActionLog
from HelperClasses import ConfigurationObject

from General import ReEnterPassword
from General import ChangePrimaryEmail
from General import Initiate_Settings_Page
from General import CheckIfTextPresentOnPage

from GetCode import GetConfirmationCode

def AddSecondaryEmail(current_emails,secondary,driver):

    if current_emails[0] == secondary:
        ActionLog("[NEW EMAIL CHANGE NOT REQUIRED] [PRIMARY EMAIL IS: {}]".format(secondary),1)
        return 1,driver
    else:
        
        if secondary in current_emails:
            ActionLog("[NEW EMAIL IS ADDED, NEEDS ROTATION]",1)
        else:
            process_status = AddSecondary(driver,secondary,ConfigurationObject.FB_USER,ConfigurationObject.FB_PASS)
            if(process_status == -1):
                TakeScreenShot(driver,CustomConstants.GetScreenShotFailedAtAddSecondary(secondary))
                return 0,driver

            ActionLog("[STATUS] [SECONDARY EMAIL ADDED]",1)
            TakeScreenShot(driver,CustomConstants.GetScreenShotSuccessAtAddSecondary(secondary))
            time.sleep(random.randint(30,40))
        
        driver, ans = RotateEmail(driver,secondary,FB_PASS)
        if(ans == -1):
            return 0,driver

        return 1,driver

def AddSecondary(driver, email, fbUser, password):
    
    
    ######### ADD EMAIL AS SECONDARY ##########
    ######### ADD EMAIL AS SECONDARY ##########
    ######### ADD EMAIL AS SECONDARY ##########
        
    ActionLog("[ADDING NEW SECONDARY EMAIL] [{}]".format(email),1)
    
    if(Insert_Secondary(driver,email) == -1):
        return -1

    if(ReEnterPassword(driver, password) == False):
        ActionLog("[FAILED AT RE-ENTER PASSWORD WHILE ADDING SECONDARY EMAIL]")
        return -1
    
    if(VerifyInsertion(driver,email) == False):
            return -1

    if(InitiatingConfirmation(driver) == -1):
        return -1
    
    if(AddingConfirmationCode(email) == -1):
        return -1

def RotateEmail(driver,secondary,FB_PASS):

    ###################################################################################
    ################################# EMAIL ROTATION ##################################
    ###################################################################################

    ActionLog("[EMAIL ROTATION STARTED]")
    driver, ans = ChangePrimaryEmail(driver, secondary, FB_PASS)
    if(ans == False):
        TakeScreenShot(driver,CustomConstants.GetScreenShotFailedAtChangePrimary(app_id))
        return driver,-1
    else:
        ActionLog("EMAIL ROTATION COMPLETE")
        TakeScreenShot(driver,CustomConstants.GetScreenShotSuccessAtChangePrimary(app_id))
    time.sleep(random.randint(30,40))
    return driver,1
    
def Insert_Secondary(driver,email):
    
    try:
        driver           = Initiate_Settings_Page(driver)
        add_email_button = driver.find_element_by_xpath(CustomConstants.AddSecondaryXpath1)
        driver.execute_script("arguments[0].click();", add_email_button)
        time.sleep(5)

        new_email_input  = driver.find_element_by_xpath(CustomConstants.AddSecondaryXpath2)
        new_email_input.send_keys(email)
        time.sleep(5)
        
        add_email_btns   = driver.find_elements_by_xpath(CustomConstants.AddSecondaryXpath3)
        for add_email_btn in add_email_btns:
            try:
                driver.execute_script("arguments[0].click();", add_email_btn)
                time.sleep(5)
                break
            except:
                pass

    except Exception as e:
        ActionLog("[FAILED AT INSERTING SECONDARY EMAIL]")
        ActionLog(str(e))
        return -1

def VerifyInsertion(driver,email):
    
    ans = CheckIfTextPresentOnPage(driver,email)
    if(not ans):
        ActionLog("[FAILED AT VERIFYING INSERTING SECONDARY EMAIL]")
        return False

def InitiatingConfirmation(driver):
    
    try:
        driver           = Initiate_Settings_Page(driver)
        confirm_button   = driver.find_element_by_xpath(CustomConstants.AddSecondaryXpath4)
        driver.execute_script("arguments[0].click();", confirm_button)
        ActionLog("[STATUS] [WAITING FOR CONFIRMATION CODE]")
        time.sleep(60)
        return 0
    except Exception as e:
        ActionLog("[FAILED AT INITIATING CONFIRMATION WHILE ADDING SECONDARY EMAIL]")
        ActionLog(str(e))
        return -1

def AddingConfirmationCode(email):

    retry         = 5
    code          = 0

    while(retry > 0):
        try:
            ActionLog("[STATUS] [STARTED RETRIEVING CONFIRMATION CODE TRY: {}]".format(str(retry)),1)
            code    = GetConfirmationCode(email)
        except Exception as e:
            ActionLog("[FAILED WHILE RETRIEVING CONFIRMATION CODE RETRY NUMBER: {}]".format(str(retry)))
            ActionLog(str(e))
        
        if code != 0 and code != None:
            code_input = driver.find_element_by_xpath(CustomConstants.ConfirmationCodeXpath1)
            ActionLog("[SERVER CODE RETRIEVED] [CODE IS: {}]".format(str(code)))
            code_input.send_keys(code)
            time.sleep(3)
            code_input.send_keys(Keys.ENTER)
            time.sleep(3)
            time.sleep(random.randint(10,15))
            break
        else:
            retry -= 1

            ##### IF NO MORE RETRIES LEFT, REMOVE THE EMAIL CONFIRMATION #####
            ##### IF NO MORE RETRIES LEFT, REMOVE THE EMAIL CONFIRMATION #####
            ##### IF NO MORE RETRIES LEFT, REMOVE THE EMAIL CONFIRMATION #####
            if(retry == 0):
                try:
                    driver             = Initiate_Settings_Page(driver)
                    time.sleep(random.randint(5,15))
                    remove_pending_btn = driver.find_element_by_xpath(CustomConstants.ConfirmationCodeXpath2)
                    driver.execute_script("arguments[0].click();", remove_pending_btn)
                    time.sleep(random.randint(10,12))
                except:
                    ActionLog("[FAILED WHILE REMOVING PENDING CONFIRMATION]")
                return -1

        time.sleep(random.randint(60,90))
    return 0
