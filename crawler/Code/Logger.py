from HelperClasses import ConfigurationObject
import os

def ResetLog():

    fpath = ConfigurationObject.DEPLOYMENT_TYPE+'/ActionLog.txt'
    fp    = open(fpath,'w')
    fp.close()

    return

def ActionLog(msg,prt=0):

    fpath  = ConfigurationObject.DEPLOYMENT_TYPE+'/ActionLog.txt'
    
    if(prt == 1):
        print(msg)

    if(not os.path.exists(fpath)):
        fp = open(fpath,'w')
        fp.close()

    ActionFile = open(fpath, 'a')
    ActionFile.write(msg + '\n' + '\n')
    ActionFile.close()

def LogClass(obj_):
    
    vals = vars(obj_)
    name = str(vals['__dict__'])
    ActionLog(name)

    for k,v in vals.items():
        if("__" in k):
            continue

        line = '\t\t'+str(k)+' : '+str(v)
        ActionLog(line)
        
    return