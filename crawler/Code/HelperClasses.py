import os

class ActiveApplication:
    
    AppId          = ""
    AppRank        = 0
    AppUrl         = ""
    OAuth          = ""
    XPath          = ""
    SecondaryEmail = ""
    AppName        = ""

class ConfigurationObject:

    DEPLOYMENT_TYPE      = "../Data/Linear" ##### DEFAULT TYPE #####
    CONFIG_PATH          = "ConfigFiles"
    EMAIL_RECEIPIENT     = ""
    FB_USER              = ""
    FB_PASS              = ""
    TROUBLE_SHOOT_COUNT  = 0
    GECKODRIVER_PATH     = ""
    FIREFOX_PROFILE_PATH = ""
    APPLICATIONS_FILE    = ""
    PROCESSED_APPS       = ""
    RESULTS              = ""
    EMAIL_DOMAIN         = ""
    NO_GO                = ""
    URL_START            = 0
    URL_END              = 0
    HL                   = True
    EMAIL_DOMAIN         = ""
    EXPERIMENT_TYPE      = ""



    def SetConfigurationObj(config):

        ConfigurationObject.TROUBLE_SHOOT_COUNT  = config["TROUBLE_SHOOT_COUNT"]
        ConfigurationObject.EXPERIMENT_TYPE      = config["EXPERIMENT_TYPE"]
        ConfigurationObject.FB_USER              = config["FB_USER"]
        ConfigurationObject.FB_PASS              = config["FB_PASS"]
        ConfigurationObject.EMAIL_RECEIPIENT     = config["EMAIL_RECEIPIENT"]
        ConfigurationObject.GEKODRIVER_PATH      = config["GEKODRIVER_PATH"]
        ConfigurationObject.FIREFOX_PROFILE_PATH = config["FIREFOX_PROFILE_PATH"]
        ConfigurationObject.EMAIL_DOMAIN         = config['EMAIL_DOMAIN']
        ConfigurationObject.NO_GO                = config['NO_GO']
        ConfigurationObject.DEPLOYMENT_TYPE      = os.path.join(config["DEPLOYMENT_TYPE"],config["EXPERIMENT_TYPE"])
        ConfigurationObject.APPLICATIONS_FILE    = os.path.join(ConfigurationObject.DEPLOYMENT_TYPE,config["APPLICATIONS_FILE"])
        ConfigurationObject.PROCESSED_APPS       = os.path.join(ConfigurationObject.DEPLOYMENT_TYPE,config["PROCESSED_APPS"])
        ConfigurationObject.RESULTS              = os.path.join(ConfigurationObject.DEPLOYMENT_TYPE,config["RESULTS"])
        ConfigurationObject.URL_START            = config["URL_START"]
        ConfigurationObject.URL_END              = config["URL_END"]
        ConfigurationObject.HL                   = config["HEADLESS"]
        ConfigurationObject.EMAIL_DOMAIN         = config["EMAIL_DOMAIN"]
        
        return