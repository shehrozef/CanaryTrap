from selenium import webdriver
from selenium.webdriver.common.by import By
from HelperClasses import ConfigurationObject
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

import time
import random

def DriverStart():
    
    options = Options()
    if(ConfigurationObject.HL):
        options.add_argument("--headless")    
    
    fp      = webdriver.FirefoxProfile(ConfigurationObject.FIREFOX_PROFILE_PATH)
    driver  = webdriver.Firefox(fp,firefox_options=options,executable_path = ConfigurationObject.GEKODRIVER_PATH)
    
    time.sleep(random.randint(1,5))
    
    return driver


def ShutDownBrowser(driver):

	try:
		driver.quit()
	except:
		pass

	return driver