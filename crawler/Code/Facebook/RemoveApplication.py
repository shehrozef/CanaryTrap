import sys
import os
import time
import random
from selenium.webdriver.common.keys import Keys
import CustomConstants

from HelperClasses import ConfigurationObject
from HelperClasses import ActiveApplication

from Logger  import ActionLog
from General import GetIFrame
from General import CheckIfTextPresentOnPage
from General import ReEnterPassword

def RemoveApplications(driver):

	success = 0
    for item in CustomConstants.Pages:
        url        	   = CustomConstants.FbTabAddr.format(item)
        ans,driver = ClickRemove(driver,url)
        if(ans == 1):
        	success = 1
    
    if(success == 0):
    	ActionLog("[FAILED] [COULD NOT REMOVE APPS FROM BOTH PAGES]")
    	return driver, 0
    return driver,1

def ClickRemove(driver,url):

	ActionLog("[STATUS] [CLICK REMOVAL OF APPS]")

    driver.get(url)
    time.sleep(10)
    driver = GetIFrame(driver)
    driver = ShowAll(driver)
    time.sleep(10)

    app_btns = driver.find_elements_by_xpath(CustomConstants.RemoveApplicationXpath2)
    if(len(app_btns) == 0):
    	ActionLog("[FAILED] [COULD NOT LOCATE ANY APPS ON APP PAGE]")
        return -1,driver

    for app_btn in app_btns:
        driver.execute_script("arguments[0].click();", app_btn)
    
    try:
        del_btn = driver.find_element_by_xpath(CustomConstants.RemoveApplicationXpath3)
        driver.execute_script("arguments[0].click();",del_btn)

        if(ReEnterPassword(driver, password) == False):
            ActionLog("[FAILED] [PASSWORD RE-ENTER FAILED IN REMOVING APPLICATIONS]")
            return -1,driver
    except:
        ActionLog("[FAILED] [COULD NOT PRESS REMOVE BUTTON IN CLICK REMOVE]")
        return -1,driver
    
    try:
        del_data = driver.find_element_by_xpath(CustomConstants.RemoveApplicationXpath4)
        driver.execute_script("arguments[0].click();",del_data)
        time.sleep(2)

        rem_btn = driver.find_element_by_xpath(CustomConstants.RemoveApplicationXpath5)
        driver.execute_script("arguments[0].click();",rem_btn)
        time.sleep(2)

        if(ReEnterPassword(driver, password) == False):
            ActionLog("[FAILED] [PASSWORD RE-ENTER FAILED IN REMOVING APPLICATIONS 2]")
            return -1,driver
    except:
        ActionLog("[FAILED] [FAILED IN DELETING APP DATA IN APP REMOVAL]")
        return -1,driver
    return 1,driver

def ShowAll(driver):
    
    show_all = CustomConstants.SAll
    while(1):
        for item in show_all:
            if(CheckIfTextPresentOnPage(driver,item) == True):
                sa_btn = driver.find_element_by_xpath(CustomConstants.RemoveApplicationXpath1.foramt(item))
                driver.execute_script("arguments[0].click();", sa_btn)
                time.sleep(10)

    return driver