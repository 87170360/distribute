import paramiko,datetime,os,ConfigParser

local_dir = os.path.abspath(os.path.dirname("__file__"))+'\upload'

#get config file
def getConfigFile(paramList):
    configList = []
    configList.append(paramList.get('sh'))
    configList.append(paramList.get('zip'))
    extFile = paramList.get('ext')
    if extFile <> None and len(extFile):
        configList = configList + extFile.split(';')
    result = []
    for name in configList:
        if name <> None and len(name) <> 0:
            result.append(name)
    return result

#upload file
def uploadFile(paramList):
    remote_dir = paramList.get('remote_dir')
    hostname   = paramList.get('hostname')
    port       = int(paramList.get('port'))
    username   = paramList.get('username')
    password   = paramList.get('password')

    try:
        print ''
        print 'uploading:'
        t = paramiko.Transport((hostname,port))
        t.connect(username=username,password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        checkList = getConfigFile(paramList)
        for f in checkList:
            print'  upload file:', f
            sftp.put(os.path.join(local_dir,f),os.path.join(remote_dir,f))
        t.close()
    except Exception:
        print"connect error!"
        os.system('pause')
        
#run sh file        
def runShFile(paramList):
    hostname   = paramList.get('hostname')
    username   = paramList.get('username')
    password   = paramList.get('password')
    sh         = paramList.get('sh')
    zipFile    = paramList.get('zip')
    remote_dir = paramList.get('remote_dir')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = hostname, username = username, password = password)

    print ''
    print 'run sh'
    if zipFile == None or len(zipFile) == 0:
        cmd = ' cd ' + remote_dir + '; /bin/sh '+ sh + ' > output' 
    else:
        cmd = ' cd ' + remote_dir + '; /bin/sh '+ sh + ' ' + zipFile + ' > output' 
    print cmd
    stdin,stdout,stderr = ssh.exec_command(cmd)

    print ''
    print 'show log'
    cmd = ' cat '+ remote_dir + 'output'
    print cmd
    stdin,stdout,stderr = ssh.exec_command(cmd)    
    print stdout.readlines()
    
    ssh.close()

#check config    
def checkOption(sec,config):
    result = True
    optionList = ['remote_dir', 'hostname','port','username','password','sh']
    for value in optionList:
        if config.has_option(sec, value) == False or len(config.get(sec, value)) == 0:
            print 'Check config.ini, no option: ' + value + ' in section: ' + sec            
            result = False
    return result

#check file exist
def checkFile(paramList, sec):
    checkList = getConfigFile(paramList)
    exist = False
    files = os.listdir(local_dir) 
    for cf in checkList:
        if len(cf) <> 0:
            exist = False
            for f in files:
                if f == cf:
                    exist = True
            if exist == False:
                print cf, 'not found in', local_dir
                print 'check config.ini section:', sec
                break
        
    return exist

#load config
def loadConfig(info):    
    config = ConfigParser.ConfigParser()
    configFile = os.path.abspath(os.path.dirname("__file__")) + '\config.ini'
    config.read(configFile)
    sections = config.sections()

    checkConfigOk = True
    checkFileOk = True

    for sec in sections:
        if checkOption(sec, config) == False:
            checkConfigOk = False
            break        
        item = {}
        for key, value in config.items(sec):
            item[key] = value

        if checkFile(item, sec) == False:
            checkFileOk = False            
            break         
        info[sec] = item
    return checkConfigOk and checkFileOk

#show_config
def showConfig(key, value):
    print key, 'config:'
    for k, v in value.items():
         print '  ' + k + ': ' + v
        
#enter point
info = {}
if loadConfig(info):
    for key, value in info.items():
        print '================================ ' + key + ' start ================================'
        showConfig(key, value)
        uploadFile(value)
        runShFile(value)
        print '================================ ' + key + ' done ================================'
        print ''

os.system('pause')


