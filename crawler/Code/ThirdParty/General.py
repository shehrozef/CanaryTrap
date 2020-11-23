import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
import random
from selenium.webdriver.common.keys import Keys
import CustomConstants

from UtilityFunctions import AddResults

from HelperClasses import ConfigurationObject
from HelperClasses import ActiveApplication

from Logger import ActionLog

def CheckAppDevStatus(driver,dev_mode_skip):

	try:
        ActionLog("[TROUBLE SHOOT] [CHEKING APP DEV STATUS]")
        driver.get(ActiveApplication.OAuth)
        time.sleep(5)

        error_txt = CustomConstants.DevModeErrorTexts
        for txt in error_txt:
        	for xpath in CustomConstants.DevModeErrorXpaths:
    			try:
    				Error_tag     = driver.find_element_by_xpath(xpath.format(txt))
    				dev_mode_skip = 1
    			except:
    				continue
        
    except Exception as e:
    	ActionLog("[FAILED] [FAILED WHILE TROUBLE SHOOTING APP DEV STATUS]")
        ActionLog(str(e))

    return driver,dev_mode_skip

def GetAppInfo(driver,ans):

    ActiveApplication.AppName = ans
    app_inf                   = {}
    app_inf['Found']          = 0
    app_type                  = "applications"

    for item in CustomConstants.Pages:
        url             = CustomConstants.FbTabAddr.format(item)
        driver,app_inf  = ExtractInfo(driver,url)
        app_type        = item

        if(app_inf['Found'] == 1):
            TakeScreenShot(driver,CustomConstants.GetScreenShotConfirmAtInstallApp(str(App_Name)))
            break

    if(app_inf['Found'] == 0):
        ActionLog("[FAILED] [COULD NOT GET APP INFO]")
        return driver,0
    else:
        app_inf['Data'].append(app_type)
        AddResults(app_inf)

    ActionLog("---------------Taking a break of 10-15 minutes----------------")
    ActionLog(str(datetime.datetime.now()))
    time.sleep(random.randint(350,600))

    return driver,1

def ExtractInfo(driver,url):

    FB_PASS  = ConfigurationObject.FB_PASS
    App_Name = ActiveApplication.App_Name
    Stuff    = []
    Result          = {}
    Result['Found'] = 0
    
    driver.get(url)
    time.sleep(10)
    
    try:
        try:
            App = driver.find_element_by_xpath(CustomConstants.AppInfoXpath1)
            driver.execute_script("arguments[0].click();", App)
        except:
            App = driver.find_element_by_xpath(CustomConstants.AppInfoXpath2)
            driver.execute_script("arguments[0].click();", App)

    except Exception as e:
        ActionLog(str(e))
        return driver,Result
    
    try:
        parent        = driver.find_element_by_xpath(CustomConstants.AppInfoXpath3)
        dialogue_html = parent.get_attribute("innerHTML")
    except Exception as e:
        dialogue_html = " "
        ActionLog()
        ActionLog()

    try:
        learn_more  = driver.find_element_by_xpath(CustomConstants.AppInfoXpath4)
        Meta        = learn_more.find_elements_by_xpath(CustomConstants.AppInfoXpath5)
        App_User_ID = Meta[1].text.split(" ")[-1].strip()
        App_User_ID = App_User_ID.strip(".")

    except Exception as e:
        App_User_ID = " "
        ActionLog()
        ActionLog()

    try:
        Contact_Page = Meta[3].find_element_by_xpath(CustomConstants.AppInfoXpath6)
        Contact_Page = Contact_Page.get_attribute("href")
    except Exception as e:
        Contact_Page = " "
        ActionLog()
        ActionLog()

    try:
        element         = driver.find_element_by_xpath("//body")
        html_whole_page = element.get_attribute('innerHTML')
    except Exception as e:
        html_whole_page = " "
        ActionLog()
        ActionLog()

    Stuff.append(App_User_ID)
    Stuff.append(Contact_Page)
    Stuff.append(App_Name)
    Stuff.append(dialogue_html)
    Stuff.append(html_whole_page)
    Result['Data'] = Stuff

    return driver,Result