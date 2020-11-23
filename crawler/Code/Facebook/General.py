import time
import random
import CustomConstants
from selenium.webdriver.common.keys import Keys

from HelperClasses import ConfigurationObject
from Logger import ActionLog


def Initiate_Settings_Page(driver):

    driver.get(CustomConstants.Facebook_Settings_Addr)
    time.sleep(random.randint(5,7))

    driver  = GetIFrame(driver)
    ans,err = OpenContactDiv(driver)
    
    if(ans == -1):
        ActionLog("[EXPERIMENT FAILED] [CONTACT DIV COULD NOT BE OPENED] [ERROR: {}]".format(err))
        TakeScreenShot(driver,CustomConstants.GetScreenShotFailedAtGetCurrentEmailStatus(secondary))
        return []

    return driver

def OpenContactDiv(driver):
    
    try:
        contact_div = driver.find_element_by_xpath(CustomConstants.ContactDivXpath)
        driver.execute_script("arguments[0].click();", contact_div)
        time.sleep(5)
        return 1,""
        
    except Exception as e:
        return -1,str(e)

def GetIFrame(driver):

    frames = driver.find_elements_by_tag_name('iframe')
    driver.switch_to_default_content()
    if(len(frames) > 0):
        driver.switch_to_frame(frames[0])
    
    return driver

def ReEnterPassword(driver, password):
    
    try:
        time.sleep(10)
        re_enter_password_div = driver.find_element_by_xpath(CustomConstants.RenterPasswordXpath)
        
        try:
            password_field    = driver.find_element_by_id('ajax_password')
            password_field.send_keys(password)
            time.sleep(3)
            password_field.send_keys(Keys.ENTER)
            time.sleep(3)
            return True
        
        except Exception as e:
            ActionLog(str(e))
            return False

    except Exception as e:
        ActionLog("[STATUS] [PASSWORD CHANGE NOT REQUIRED]")
        return True

def CheckIfTextPresentOnPage(driver, txt):
    
    try:
        driver.find_element_by_xpath(CustomConstants.TextTempXpath.format("*",txt))
        return True
    except Exception as e:
        ActionLog(str(e),0)
        return False

def ChangePrimaryEmail(driver, current_secondary_email, password):
    
    try:
        driver                      = Initiate_Settings_Page(driver)
        secondary_email_input_label = driver.find_element_by_xpath(CustomConstants.ChangePrimaryXpath1.format(current_secondary_email))
        secondary_email_input_label = driver.find_element_by_xpath(CustomConstants.ChangePrimaryXpath2)
        driver.execute_script("arguments[0].click();", secondary_email_input_label)
        time.sleep(2)
        
        if(ReEnterPassword(driver, password) == False):
            ActionLog("[FAILED AT RE-ENTER PASSWORD WHILE CHANGING PRIMARY EMAIL]")
            return driver,False
        time.sleep(random.randint(3,7))
        return driver,True
        
    except Exception as e:
        ActionLog("[FAILED] [EMAIL: {} NOT ROTATED TO PRIMARY]".format(current_secondary_email))
        ActionLog(str(e))
        return driver,False