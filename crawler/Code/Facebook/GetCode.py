import re
import os
import sys
import time
import json
import pytz
import email
import pysftp
import datetime

from HelperClasses import ConfigurationObject
from Logger import ActionLog

def Load_Config():
    
    config_filename = "config_email_server.json"
    fpath           = os.path.join(ConfigurationObject.DEPLOYMENT_TYPE,ConfigurationObject.CONFIG_PATH,config_filename)
    config          = {}

    ActionLog("[LOADING DATA] [LOADING EMAIL SERVER CONFIG FILE {}]".format(config_filename))
    
    with open(fpath,'r') as file:

        config = json.load(file)
    
    ActionLog("[LOADED DATA] [EMAIL SERVER CONFIGURATION DATA LOADED]")

    return config

def DigitalOceanConnection():
    
    config          = Load_Config()
    
    host            = config["HOST"]
    password        = config["PASSWORD"]
    username        = config["USERNAME"]
    dir_mails       = config["DIR_MAILS"]
    
    cnopts          = pysftp.CnOpts()
    cnopts.hostkeys = None
    sftp            = pysftp.Connection(host, username=username, password=password,cnopts=cnopts)
     
    return sftp,dir_mails

def GetConfirmationCode(sender_id):
    
    #User_id is useless function. I have added this to remove
    
    Files_List     = []
    LocalMailDir   = 'emails/'
    Sftp,Dir_Mails = DigitalOceanConnection()
    
    ActionLog("[SERVER CONNETED]",1)
    
    try:
        
        ########## GET NEW EMAILS FROM SERVER ##########
        ########## GET NEW EMAILS FROM SERVER ##########
        ########## GET NEW EMAILS FROM SERVER ##########

        Sftp.cwd(Dir_Mails)
        data = Sftp.listdir()
        
        for fileName in data:
            timest = fileName.split('.')[0]
            Files_List.append((int(timest),fileName))
            
        ########## SORT FILES BASED ON TIME STAMP ##########
        ########## SORT FILES BASED ON TIME STAMP ##########
        ########## SORT FILES BASED ON TIME STAMP ##########

        Files_List = sorted(Files_List, key=lambda tup: tup[0],reverse=True)
        st         = time.time()
        st         = int(st) - 900
        dist       = 1000000
        res        = 0

        for fileObj in Files_List:
            if fileObj[0] > st:
                if((st - fileObj[0]) < dist):
                    dist = st - fileObj[0]
                    
                    sftp.get(fileObj[1],'email')
                    b = email.message_from_file(open('email'))
                    to_ = b['to']
                    subject_ = b['subject']
                    
                    if "New email address added on Facebook" == subject_ and sender_id in to_:
                        for part in b.walk():
                            # each part is a either non-multipart, or another multipart message
                            # that contains further parts... Message is organized like a tree
                            if part.get_content_type() == 'text/plain':
                                print("Parsing Email")
                                msg_str = part.get_payload()
                                p = re.compile("You may be asked to enter this confirmation code: (.*).Confirm")
                                result = p.findall(msg_str)
                                
                                res =  result[0]
        sftp.close()
        return res
    except Exception as e:
        ActionLog(str(e))
        return 0