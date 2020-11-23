import os
import csv
import sys
import time
import json
import uuid
import random
import datetime
import CustomConstants

from collections import OrderedDict

from HelperClasses import ActiveApplication
from HelperClasses import ConfigurationObject

from UtilityFunctions import LoadConfigData
from UtilityFunctions import VerifyExperimentType
from UtilityFunctions import VerifyDeployementFolder
from UtilityFunctions import GetAppsToInstall
from UtilityFunctions import GetCurrentAccountState

from SeleniumFunctions import DriverStart
from SeleniumFunctions import ShutDownBrowser

from Facebook.Login import Account_Login
from Facebook.AddSecondary import AddSecondaryEmail
from Facebook.InstallApplication import InstallApp
from Facebook.RemoveSecondary import RemoveAllSecondary
from Facebook.RemoveApplication import RemoveApplications

from ThirdParty.General import CheckAppDevStatus
from ThirdParty.General import GetAppInfo

from Logger import ActionLog
from Logger import ResetLog
from Logger import LogClass

def InitiateExperiment(config):
    
    
    ActionLog("[STATUS] [EXPERIMENT HAS BEEN INITIATED]",1)
    
    ##### GET APPS TO INSTALL #####
    

    apps_to_install, no_go_apps, timer = GetAppsToInstall()

    for app_details in apps_to_install:

        
        ActiveApplication.AppId          = app_details[0]
        ActiveApplication.AppRank        = app_details[1]
        ActiveApplication.AppUrl         = app_details[2]
        ActiveApplication.OAuth          = app_details[3]
        ActiveApplication.XPath          = app_details[4]
        ActiveApplication.SecondaryEmail = app_details[5]
        dev_mode_skip                    = 0
        LogClass(ActiveApplication)

        ##### No_Go Apps are the ones that are broken, so we avoid them #####
        ##### These apps are added by ThirdPart/General.py when crawling a website fails.
        

        if(ActiveApplication.AppId in no_go_apps):
            continue        

        ActionLog("[PROCESSING] [APPLICATION: {} App Name: {}]".format(ActiveApplication.AppId,ActiveApplication.AppUrl))

        ###################################################################################
        ############################### ACCOUNT LOG IN ####################################
        ###################################################################################
        
        driver           = DriverStart()
        ans              = Account_Login(driver)

        if(ans == 0):
            return 0,driver

        ###################################################################################
        ############################### GET CURRENT SATAE #################################
        ###################################################################################
        ## Crawler can crash at any point while assigning secondary or primary email.
        ## This current state help in determining the point of crash and restart code accordingly.

        # Returns list of email addresses already added in the Facebook account

        ans              = GetCurrentAccountState(driver, ConfigurationObject.FB_PASS)
        secondary        = ActiveApplication.SecondaryEmail+"@"+ConfigurationObject.EMAIL_DOMAIN

        if(ans == []):
            return 0,driver
            
        ################## Add Secondary Email ############################
        ################## Add Secondary Email ############################
        ################## Add Secondary Email ############################

        # Adds the new honeytoken (email address) to the Facebook account

        ans,driver       = AddSecondaryEmail(ans,secondary,driver)

        if(ans == 0):
            return 0,driver
        
        ###################################################################################
        ################################# Install Application# ############################
        ###################################################################################
        
        ans,driver               = InstallApp(driver,secondary)
        
        # This checks if the application failed because of external issues or not

        if(ans == -1):
            driver,dev_mode_skip = CheckAppDevStatus(driver,dev_mode_skip)

        # If app was installed we get all the information about it from Facebook

        if(dev_mode_skip == 0):
            driver = GetAppInfo(driver,ans)

        ##################### WE KEEP ONLY 5 EMAILS IN ONE ACCOUNT AT A TIME #############
        #### While we keep 5 emails at once, only one is leaked which is set as primary.

        
        # To avoid getting banned by Facebook, we restrict to keeping 5 email addresses in one account at a time
        # If we have 5 honeytokens at one time, we remove them all and reset to just 1
        
        timer += 1
        if(timer % 5 == 0):
            driver,ans = RemoveAllSecondary(driver)
            if(ans == -1):
                return 0,driver


        ###################################################################################
        ############################### REMOVE APPLICATIONS ###############################
        ###################################################################################

        ShutDownBrowser(driver)
        driver           = DriverStart()
        ans              = Account_Login(driver)

        if(ans == 0):
            return 0,driver

        driver,ans       = RemoveApplications(driver) 
        if(ans == 0):
            return 0,driver

        res              = AddProNames(dev_mode_skip)
        if(res == 0):
            return 0,driver
     
    
    return 1,driver


def Start(config_filename):

    config = LoadConfigData(config_filename)

    ##### VERIFICATION OF EXPERIMENT #####
    ##### VERIFICATION OF EXPERIMENT #####
    ##### VERIFICATION OF EXPERIMENT #####

    # This is to check if the experiment (linear or matrix) is defined properly or not
    

    if(not VerifyDeployementFolder(ConfigurationObject.DEPLOYMENT_TYPE) or not VerifyExperimentType(ConfigurationObject.EXPERIMENT_TYPE)):
        return 0


    ##### PROCESS APPS TILL LIST ENDS #####
    ##### PROCESS APPS TILL LIST ENDS #####
    ##### PROCESS APPS TILL LIST ENDS #####

    res,driver = InitiateExperiment(config)
    ShutDownBrowser(driver)
    return res,driver

    
if __name__ == "__main__":

    try:
        ResetLog()
        ActionLog("[STATUS] [ENTER MAIN FUNCTION]")
        
        config_filename  = sys.argv[1]
        driver           = ""
        
        ActionLog("[STATUS] [EXPERIMENT START FUNCTION CALLED]")
        ans,driver = Start(config_filename)

    except Exception as e:

        ##### MAKE A FUNCTION IN UTIL #####
        ##### MAKE A FUNCTION IN UTIL #####
        ##### MAKE A FUNCTION IN UTIL #####
        ActionLog("Some unknown exception occurred. Error Message: "+str(e))