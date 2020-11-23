import re
import sys
import csv
import json
import time
import random
from requests import get

import CustomConstants

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException

from SeleniumFunctions import DriverStart
from SeleniumFunctions import ShutDownBrowser
from HelperClasses import ConfigurationObject
from HelperClasses import ActiveApplication
from Logger import ActionLog


def InstallApp(driver,email):
    
    ActionLog("[STATUS] [STARTED INSTALLATION APP FUNCTION]")

    ### TRY CHECKING AVAILABILITY WITH OLD XPATH ###
    ### TRY CHECKING AVAILABILITY WITH OLD XPATH ###
    ### TRY CHECKING AVAILABILITY WITH OLD XPATH ###

    driver,answer = ProcessWebsite(driver,[ActiveApplication.OAuth],ActiveApplication.XPath,ActiveApplication.AppRank)
    if(answer['Found'] == -1):
    	ActionLog("[FAILED AT INSTALL APPLICATION WITH OLD XPATH]",1)
		

    ### TRY INSTALL APPLICATION WITH DEFAULT XPATH ###
    ### TRY INSTALL APPLICATION WITH DEFAULT XPATH ###
    ### TRY INSTALL APPLICATION WITH DEFAULT XPATH ###
    if(answer['Found'] != 1):
    	ShutDownBrowser(driver)
    	driver        = DriverStart()
    	driver,answer = ProcessWebsite(driver,[ActiveApplication.OAuth],CustomConstants.MakeCheckStr(),ActiveApplication.AppRank)
    	if(answer['Found'] == -1):
    		ActionLog("[FAILED AT INSTALL APPLICATION WITH NEW XPATH]",1)

    
    if(answer['Found'] != 1):
        return -1,driver
    else:
        return str(answer['App_Name']),driver

def ProcessWebsite(driver,urls,check_str,rank):
	
	for url in urls:

		ActionLog("[STARTING PROCESSING URL: {}]".format(url))

		driver,result  = IsOauth(driver,result,url)
		
		if(result['Found'] != 0):
			return driver,result
		
		try:
			check_str 	      = CleanCheckStr(check_str)
			tags 			  = driver.find_elements_by_xpath(check_str)
			try:
				driver,result = Process_Clicks(driver,tags, url ,rank, 0)
				
				if(result['Found'] == 2):
				
					while(result['Found'] == 2):
						
						ActionLog("[RE-PROCESSING URL {} FROM TAGS {} ONWARDS]".format(url,str(result['Skips'])))
						ShutDownBrowser(driver)
						driver        = DriverStart()
						driver.get(url)
						sleep(5)
						tags   		  = driver.find_elements_by_xpath(check_str)
						driver,result = Process_Clicks(driver, tags, url ,rank, result['Skips'])
				
				if(result['Found'] == 1):
					return driver,result

			except Exception as e:
				ActionLog("[FAILED AT PROCESSING OAUTH WHILE PROCESSING CLICKS]")
				ActionLog(str(e))
				continue


		except Exception as e:
			ActionLog("[FAILED AT RETRIEVING TAGS IN PROCESSING THE OAUTH WEBSITE]")
			ActionLog(str(e))
			return driver,result

	return driver,result

def CleanCheckStr(check_str):
	
	try:
		c             = check_str
		parts         = c.split("[")
		tag_name      = parts[0]
		parts 		  = parts[1].split(") or")
		parts[-1] 	  = parts[-1].replace("]","")
		parts[-1]     = parts[-1] + ")"
		parts[-1]     = parts[-1].replace("))","")
		new_check_str = tag_name+"["
		arr 		  = []
		
		for p in parts:
			p = p.strip(" ")
			p = p+")"
			q = (p.split("'")[1])
			if(q != ""):
				arr.append(p)
		
		conds 		   = " or ".join(arr)
		new_check_str += conds+"]"

	except:
		ActionLog("[FAILED AT CLEANING OLD STRING]")
		return check_str
	
	return new_check_str

def IsOauth(driver,url):
	
	result 			   = {}
	result['Found']    = 0
	result['Skips']    = 0
	result['App_Name'] = 0
	
	try:
		driver.get(url)
		time.sleep(3)
		
		curr_url = driver.current_url
		handles  = driver.window_handles
		
		if(CustomConstants.URL_KEYWORD in curr_url):
			driver,result = FindContinue(driver,result,0,handles,0)
			return driver,result

		return driver,result

	except Exception as e:
		ActionLog("[ERROR WHILE OPENING OAUTH URL] [{}]".format(url))
		time.sleep(3)
		result['Found'] = -1
		return result

def Reduce(arr,max_limit,number):
	
	new_tags = []
	arr 	 = arr[:max_limit]
	for tag in arr[number:]:
		if(tag.tag_name in CustomConstants.SKIP_TAGS):
			continue
		else:
			new_tags.append(tag)

	return new_tags

def CloseWindowsExceptFirst(driver):
	
	number_of_handles = len(driver.window_handles)
	for x in range(1,number_of_handles):
		driver.switch_to.window(driver.window_handles[x])
		driver.close()
	driver.switch_to.window(driver.window_handles[0])
	return driver

def FindContinue(driver,result,handles,temp_url='null'):

	_handles = driver.window_handles
	if(len(_handles) > 2):
		ActionLog("[FAILED] [TOO MANY WINDOWS IN FINDING CONTINUE BUTTON]")
		result['Found'] = -1
		return driver,result

	if(len(handles) != len(_handles)):
		driver,result = HandlePopUp(driver,_handles,result)
	else:
		driver,result = HandleNoPopUp(driver,temp_url,result)
	
	return driver,result

def HandlePopUp(driver,_handles,result):

	ActionLog("[STATUS] [HANDLING POP UP] [SHIFTING TO WINDOW WITH URL {}]".format(driver.current_url))
	try:
		time.sleep(5)
		driver.switch_to.window(_handles[-1])
		
		if(CustomConstants.URL_KEYWORD in driver.current_url): 
			driver,result   = ProcessContinueTag(driver,result)
			return driver,result
		
		else:
			driver 			= CloseWindowsExceptFirst(driver)
			return driver, result

	except Exception as e:
		ActionLog("[FAILED IN HANDLING POP UP. CHECK DRIVER CLOSE / MANAGEMENT]")
		ActionLog(str(e))
		result['Found'] = -1
		return driver,result

def HandleNoPopUp(driver,temp_url,result):

	ActionLog("[STATUS] [HANDLING NON-POP UP] [SHIFTING TO WINDOW WITH URL {}]".format(driver.current_url))
	try:
		sleep(5)
		if(CustomConstants.URL_KEYWORD in driver.current_url):
			driver,result   = ProcessContinueTag(driver,result)

		if(result['Found'] == -1):
			result['Found'] = 2
		
		return driver,result

	except Exception as e:
		ActionLog("[FAILED IN HANDLING NO-POP UP. CHECK DRIVER CLOSE / MANAGEMENT]")
		ActionLog(str(e))
		result['Found'] = -1
		return driver,result

def ProcessContinueTag(driver,result):

	button_not_div = 1
	try:
		try:
			Install_btn = driver.find_element_by_xpath(CustomConstants.INSTALLATION_XPATH1)
		except:
			Install_btn = driver.find_element_by_xpath(CustomConstants.INSTALLATION_XPATH2)
			button_not_div = 0

		try:
			try:
				App_Name = driver.find_element_by_xpath(CustomConstants.INSTALLATION_XPATH3)
				App_Name = str(App_Name.text).strip()
			except:
				App_Name = driver.find_element_by_xpath(CustomConstants.INSTALLATION_XPATH4)
				App_Name = (App_Name.text).split("'s")[0]


			driver.execute_script("arguments[0].click();", Install_btn)
			result['App_Name'] = App_Name
			result['Found']	   = 1
			sleep(30)

			if(button_not_div == 1):
				driver = PressContinueTag(driver,CustomConstants.INSTALLATION_XPATH5)
			else:
				driver = PressContinueTag(driver,CustomConstants.INSTALLATION_XPATH6)

			return driver,result

		except Exception as e:
			ActionLog("[FAILED AT FINDING APP NAME IN FIND CONTINUE FUNCTION]")
			ActionLog(str(e))
			result['Found'] = -1
			return driver,result

	except Exception as e:
		driver = CloseWindowsExceptFirst(driver)
		ActionLog("[FAILED] [COULD NOT FIND CONTINUE AS BUTTON ANYWHERE]")
		ActionLog(str(e))
		result['Found'] = -1
		return driver,result

def PressContinueTag(driver,str_xpath):
	
	try:
		while(1):
			Double_Confirm = driver.find_element_by_xpath(str_xpath)
			driver.execute_script("arguments[0].click();", Double_Confirm)
			sleep(10)
	except Exception as e:
		
		sleep(15)
		driver.switch_to.window(driver.window_handles[0])
		return driver

def Process_Clicks(driver,tags,url,rank,tag_skips):
	
	result             = {}
	result['Skips']	   = tag_skips
	result['App_Name'] = 0
	result['Found']    = 0
	tag_index          = tag_skips
	tags 			   = Reduce(tags,50,tag_skips)
	
	for tag in tags:
	
		tag_text 		   = tag.text
		tag_name 		   = tag.tag_name
		
		try:
			ActionLog("Tag Text: {}".format(tag_text))
			ActionLog("Tag Name: {}".format(tag_name))
			
			handles   = driver.window_handles
			temp_url  = driver.current_url
			tag_index = tag_index + 1

			sleep(5)
			driver.execute_script("arguments[0].click();", tag)
			sleep(5)

		except Exception as e:
			continue

		driver,result = FindContinue(driver,result,handles,temp_url)
		if(result['Found'] != 0):
			result['Skips'] = tag_index
			break

	return driver,result


