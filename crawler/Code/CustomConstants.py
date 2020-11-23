### EXPERIMENT TYPE CONSTANTS ###
LinearExperiment = "Linear"
MatrixExperiment = "Matrix"

### ERROR MESSAGES CONSTANTS ###
LogFailedAtLogin                 = "Failed While Attempting to Login:"
LogFailedAtGetCurrentEmailStatus = "Failed While Getting Current Status Of Emails:"
LogFailedAtOpenContactDiv        = "Failed while Opening Contact Div"
LogFailedAtAddSecondary          = "Failed while Adding Secondary Email"
LogFailedAtRemoveSecondary       = "Failed while Removing Secondary Emails"
LogFailedAtChangePrimary         = "Failed while Changing Primary Email"
LogFailedAtRemovePending         = "Failed while Removing Pending Email"
LogFailedAtRemoveApplications    = "Failed while Removing Applications"
LogFailedAtProcApplications      = "Failed while Processing Applications"
LogFailedAtInstallApplications   = "Failed while Install Applications"
LogFailedAtGetAppInfo            = "Something failed at app info"
LogFailedAtTroubleShoot          = "Trouble shoot too many times"
LogTerminateMessage              = "Finished Experiment"
LogUrgentHalt                    = "WRONG SECONDARY EMAIL HAS BEEN ASSIGNED. URGENT CHECK "

### FACEBOOK CONSTANTS ###
Facebook_Addr          = "https://www.facebook.com"
Facebook_Settings_Addr = "https://www.facebook.com/settings"
URL_KEYWORD            = "oauth"

### TAGS TO BE SKIPPED LIST ###
SKIP_TAGS = ["script","style","noscript","symbol"]

### INSTALLATION XPATHS ###
INSTALLATION_XPATH1 = "//button[contains(text(), 'Continue as')]"
INSTALLATION_XPATH2 = "//div[contains(text(), 'Continue as')]"
INSTALLATION_XPATH3 = "//span[@class='fwb']"
INSTALLATION_XPATH4 = "//div[contains(text(),'Privacy')]/../.."
INSTALLATION_XPATH5 = "//button[@name='__CONFIRM__']"
INSTALLATION_XPATH6 = "//button[@data-testid='nextBtn']"

### REMOVE ALL SECONDARY XPATHS ###
RemoveAllSecondaryXpath1 = '//div[contains(@class,"_8vbq")]'
RemoveAllSecondaryXpath2 = '//span[contains(text(),{})]/..'
RemoveAllSecondaryXpath3 = './/a' 

### FACEBOOK FUNCTION XPATH CONSTANTS ###
ContactDivXpath         = "//h3[contains(text(), 'Contact')]"
RenterPasswordXpath     = "//*[contains(text(), 'you must re-enter your')]"
TextTempXpath           = "//{}[contains(text(), '{}')]"

ConfirmationCodeXpath1  = "//input[@name='code']"
ConfirmationCodeXpath2  = "//a[@class='SettingsEmailPendingCancel']"

ChangePrimaryXpath1     = "//span[contains(text(), '{}')]"
ChangePrimaryXpath2     = "./div/a"
ChangePrimaryXpath3     = "//input[@value='Save Changes']"

GetCurrentStateXpath1   = "//span[contains(text(),'Current Emails')]/../.."
GetCurrentStateXpath2   = ".//div"

AddSecondaryXpath1      = "//a[contains(text(), 'another email')]"
AddSecondaryXpath2      = "//input[@name='new_email']"
AddSecondaryXpath3      = "//button[contains(text(), 'Add')]"
AddSecondaryXpath4      = "//a[contains(text(), 'Confirm')]"

RemoveApplicationXpath1 = "//*[contains(text(), '{}')]"
RemoveApplicationXpath2 = "//button[@role='checkbox']"
RemoveApplicationXpath3 = "//div[contains(text(), 'Remove')]"
RemoveApplicationXpath4 = "//input[@name='delete_activity']"
RemoveApplicationXpath5 = "//button[@name='confirmed']"

SAll                    = ["Show all","show all", "show-all", "Show-all", "Show All"]

### DEV MODE COSNTATNS ###
DevModeErrorTexts  = ["Error","App not","Login Failed","secure connection","load URL:"]
DevModeErrorXpaths = [
                        "//h3[contains(text(), '{}')]", 
                        "//span[contains(text(), '{}')]",
                        "//div[contains(text(), '{}')]"
                     ]

### APP INFO CONSTANTS ###
Pages         = ["applications","business_tools"]
FbTabAddr     = "https://www.facebook.com/settings?tab={}"
AppInfoXpath1 = "//*[contains(text(),{})]"
AppInfoXpath2 = '//*[contains(text(),{})]'
AppInfoXpath3 = "//*[contains(text(),'Email')]/../../../../../../../.."
AppInfoXpath4 = "//*[contains(text(),'Get help')]/.."
AppInfoXpath5 = './/div'
AppInfoXpath6 = './/a'

### TAKESCREENSHOT CONSTANTS ###
def GetScreenShotDevModeApp(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "DevMode_App_"+str(identifier)
    
def GetScreenShotAddedWrongEmail(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Wrong_Email_"+str(identifier)

def GetScreenShotFailedAtLoginPrefix(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Failed_Login_"+str(identifier)

def GetScreenShotFailedAtProcApplication(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Failed_Proc_Application_"+str(identifier)

def GetScreenShotFailedAtRemoveApplications(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Failed_Remove_Applications_"+str(identifier)

def GetScreenShotSuccessAtRemoveApplications(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Success_Remove_Applications_"+str(identifier)

def GetScreenShotFailedAtRemovePending(identifier= None):
    if identifier == None:
        identifier = 'noId'
    return "Failed_Pending_Remove_"+str(identifier)

def GetScreenShotFailedAtGetCurrentEmailStatus(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Get_Current_Email_Status_"+str(identifier)

def GetScreenShotFailedAtOpenContactDiv(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Open_Contact_Div_"+str(identifier)

def GetScreenShotFailedAtRemoveSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Remove_Secondary_"+str(identifier)

def GetScreenShotSuccessAtRemoveSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Success_Remove_Secondary_"+str(identifier)

def GetScreenShotFailedAtAddSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Add_Secondary_"+str(identifier)

def GetScreenShotSuccessAtAddSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Success_Add_Secondary_"+str(identifier)

def GetScreenShotFailedAtChangePrimary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Change_Primary_"+str(identifier)

def GetScreenShotSuccessAtChangePrimary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Success_Change_Primary_"+str(identifier)

def GetScreenShotFailedAtInstallApp(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_Install_App_"+str(identifier)

def GetScreenShotSuccessAtInstallApp(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Success_Install_App_"+str(identifier)

def GetScreenShotFailureAtRemoveAllSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Failed_At_All_Sec_Removal_"+str(identifier)

def GetScreenShotSuccessAtRemoveAllSecondary(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Success_At_All_Sec_Removal_"+str(identifier)

def GetScreenShotConfirmAtInstallApp(identifier=None):
    if identifier == None:
        identifier = 'noapp'
    return "Confirm_Install_App_"+str(identifier)


### INSTALLATION XPATH CHECK STR ###
def MakeCheckStr():
    Check_Str  = "//*["
    tags   = ["@href","@class","@id","text()"]
    kwords = ["fb","facebook","Facebook"]
    for t in tags:
        for k in kwords:
            Check_Str += "contains({}, '{}') or ".format(t,k)
    Check_Str = Check_Str.strip(" or ")
    Check_Str += "]"
    return Check_Str