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

def RemoveAllSecondary(driver,secondary=None):
    
    ActionLog("[STATUS] [REMOVING ALL UNWANTED EMAILS]",1)
    try:
        driver 									   = Initiate_Settings_Page(driver)
        emails_ignore   						   = {}
        emails_ignore[ConfigurationObject.FB_USER] = 1
        if secondary != None:
            emails_ignore[secondary] 			   = 1
    except Exception as e:
        ActionLog("[FAILED] [FAILED AT STARTING ON REMOVING ALL SECONDARY EMAILS]")
        return driver,-1

    driver,ans = ChangePrimaryEmail(driver,ConfigurationObject.FB_USER)
    if(ans == False):
        return driver,-1
    
    driver,ans = ClickRemove(driver,emails_ignore)
    if(ans == -1):
        return driver,-1
    
    time.sleep(random.randint(4,16))
    return driver,1

def ClickRemove(driver,emails_ignore):

    driver      = Initiate_Settings_Page(driver)
    email_items = driver.find_element_by_xpath(CustomConstants.RemoveAllSecondaryXpath1)
    for email in email_items:
        txt     = str(email.text.split("\n")[0])
        if(txt not in emails_ignore):
            try:
                parent = driver.find_element_by_xpath(CustomConstants.RemoveAllSecondaryXpath2.format(txt))
                remtag = parent.find_elements_by_xpath(CustomConstants.RemoveAllSecondaryXpath3)[-1]
                driver.execute_script("arguments[0].click();", remtag)
                time.sleep(random.randint(3,9))
            except Exception as e:
                ActionLog("[FAILED] [WHILE CLICKING REMOVE IN REMOVING ALL SECONDARY]")
                ActionLog(str(e))
                return driver,-1
    return driver,1