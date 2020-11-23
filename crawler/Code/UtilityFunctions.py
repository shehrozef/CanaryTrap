import os
import csv
import sys
import json
import uuid
import time
import random
import datetime
import CustomConstants

from collections import OrderedDict

from HelperClasses import ActiveApplication
from HelperClasses import ConfigurationObject

from Facebook.General import OpenContactDiv
from Facebook.General import GetIFrame
from Facebook.General import Initiate_Settings_Page

from Logger import ActionLog
from Logger import LogClass


def LoadConfigData(config_filename):

    fpath = os.path.join(ConfigurationObject.DEPLOYMENT_TYPE,ConfigurationObject.CONFIG_PATH,config_filename)

    ActionLog("[LOADING DATA] [LOADING CONFIG FILE {}]".format(config_filename))
    
    with open(fpath,'r') as file:

        config = json.load(file)
    
    ActionLog("[LOADED DATA] [CONFIGURATION DATA LOADED]")

    ConfigurationObject.SetConfigurationObj(config)

    LogClass(ConfigurationObject)

    return config

def VerifyDeployementFolder(DEPLOYMENT_TYPE):

    ##### UPDATE CLASS VARIABLES WITH CONFIG #####
    ##### UPDATE CLASS VARIABLES WITH CONFIG #####
    ##### UPDATE CLASS VARIABLES WITH CONFIG #####
    ConfigurationObject.DeploymentType = DEPLOYMENT_TYPE
    if(not os.path.exists(DEPLOYMENT_TYPE)):
        ActionLog("[ERROR FILE SETUP] [PLEASE CREATE DEPLOYMENT DIRECTORY {}] [UPDATE FOLDER WITH FILES]".format(DEPLOYMENT_TYPE),1)
        ActionLog("[EXITING WITH ERROR]",1)
        return 0
    return 1

def VerifyExperimentType(EXPERIMENT_TYPE):
    
    ##### VERIFY EXPERIMENT INITIATED CORRECT #####
    ##### VERIFY EXPERIMENT INITIATED CORRECT #####
    ##### VERIFY EXPERIMENT INITIATED CORRECT #####
    
    if (not (EXPERIMENT_TYPE == CustomConstants.LinearExperiment or EXPERIMENT_TYPE == CustomConstants.MatrixExperiment)):
        ActionLog("[ERROR CONFIGURATION] [EXPERIMENT TYPE IS POORLY CONFIGURED]")
        ActionLog("[EXITING WITH ERROR]",1)
        return 0
    return 1

def GetApps():

    s                 = ConfigurationObject.URL_START
    e                 = ConfigurationObject.URL_END
    APPLICATIONS_FILE = ConfigurationObject.APPLICATIONS_FILE

    ActionLog("[LOADING APPLICATIONS_FILE] [APPLICATIONS_FILE {}]".format(APPLICATIONS_FILE))
    
    i=1
    apps = []
    with open(APPLICATIONS_FILE) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        next(reader)
        
        for row in reader:
            if(i>=s and i<=e):
                apps.append(row)
            i += 1

    ActionLog("[LOADED APPLICATIONS_FILE] [APPLICATIONS_FILE PATH {}]".format(APPLICATIONS_FILE),1)

    return apps

def GetProcessedApps():

    ##### RETURNS APP_ID and EMAIL #####
    ##### RETURNS APP_ID and EMAIL #####
    ##### RETURNS APP_ID and EMAIL #####
    
    PATH  = ConfigurationObject.PROCESSED_APPS
    names = {}
    ActionLog("[LOADING PROCESSED_APPS] [PROCESSED_APPS {}]".format(PATH))
    
    
    if(not os.path.exists(PATH)):
        f      = open(PATH,'w')
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["App_ID","Rank","App","Oauth","Xpath",'Email','Time','Dev Type'])
        f.close()

    with open(PATH,'r') as f:
        reader = csv.reader(f,delimiter=",")
        next(reader)
        for row in reader:
            names[row[0]] = row[5]
    ActionLog("[LOADED PROCESSED_APPS] [PROCESSED_APPS {}]".format(PATH),1)
    
    return names

def GetNoGoApps():

    NO_GO      = ConfigurationObject.NO_GO
    no_go_apps = {}
    if(os.path.exists(NO_GO) == True):
        with open(NO_GO,'r') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            for row in csv_reader:
                no_go_apps[row[0]] = 1

    return no_go_apps

def GetAppsToInstall():

    all_apps        = GetApps()
    processed_apps  = GetProcessedApps()
    no_go_apps      = GetNoGoApps()
    apps_to_install = []
    timer           = 0
    
    for k in all_apps:
        if(k[0] not in processed_apps):
            apps_to_install.append(k)
        else:
            timer+=1

    return apps_to_install, no_go_apps, timer
    
def TakeScreenShot(driver,fileName,DEPLOYMENT_TYPE=None):
    
    screenshot_folder = ConfigurationObject.DEPLOYMENT_TYPE + "/Screenshots/"
    fileName = str(int(time.time()))+'_'+fileName+'.png'
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    driver.get_screenshot_as_file(screenshot_folder+fileName)

def GetCurrentAccountState(driver, FB_PASS):
    
    driver = Initiate_Settings_Page(driver)
    
    try:
        parent_div = driver.find_element_by_xpath(CustomConstants.GetCurrentStateXpath1)
        email_divs = parent_div.find_elements_by_xpath(CustomConstants.GetCurrentStateXpath2)
        emails     = []

        for i in range(len(email_divs)):
            if(i%2 != 0):
                text = email_divs[i].text
                e = text.split("\n")[0]
                emails.append(e)

        return emails

    except Exception as e:
        ActionLog("[EXPERIMENT FAILED] [GETTING CURRENT STATE FAILED]")
        ActionLog("[ERROR: "+str(e)+"]")
        TakeScreenShot(driver,CustomConstants.GetScreenShotFailedAtGetCurrentEmailStatus(secondary))
        return []

def CheckStatus(driver):

    primary_email,current_emails = GetCurrentAccountState(driver, ConfigurationObject.FB_PASS)
    
    ActionLog("[STATUS] [FACEBOOK ACCOUNT CURRENT STATE]")
    ActionLog("[CURRENT PRIMARY] ["+str(primary_email)+"]")
    ActionLog("[CURRENT PRIMARY] ["+str(len(current_emails))+"]")

    return primary_email,current_emails
    
def AddResults(stuff):

    with open(ConfigurationObject.RESULTS,'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow([stuff[0],stuff[1],stuff[2],stuff[5],ActiveApplication.AppId,ActiveApplication.AppUrl,ActiveApplication.AppRank,ActiveApplication.SecondaryEmail])
    
    if not os.path.exists(ConfigurationObject.DeploymentType+'/AppsData/HTML_Dialog/'):
        os.makedirs(ConfigurationObject.DeploymentType+'/AppsData/HTML_Dialog/')
    
    if not os.path.exists(ConfigurationObject.DeploymentType+'/AppsData/HTML_Page/'):
        os.makedirs(ConfigurationObject.DeploymentType+'/AppsData/HTML_Page/')

    with open(ConfigurationObject.DeploymentType+"/AppsData/HTML_Dialog/{}.html".format(ActiveApplication.AppName),'w') as file:
        file.write(stuff[3])
    
    with open(ConfigurationObject.DeploymentType+"/AppsData/HTML_Page/{}.html".format(ActiveApplication.AppName),'w') as file:
        file.write(stuff[4])

def AddProNames(dev_mode):

    try:
        f = open(ConfigurationObject['PROCESSED_APPS'],'a')
        writer = csv.writer(f, delimiter=",")
        
        cleaned = []
        for attr in dir(ActiveApplication):
            if(attr.startswith('__')):
                continue
            cleaned.append(str(ActiveApplication[attr]).replace("\n"," "))

        writer.writerow([cleaned[0],cleaned[1],cleaned[2],cleaned[3],cleaned[4],cleaned[5],cleaned[6],str(datetime.datetime.now()),str(dev_mode)])
        f.close()
        return 1

    except Exception as e:
        ActionLog(str(e))
        ActionLog("[FAILED AT ADDING PROCESSED APP TO CSV]")
        return 0
