import json, random, string
from credentials import *

def LimitedJSONInfo(Load=""):
    serverCredentials = getJsonInformation()
    if Load == "about":
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("AboutMe"))) as aboutMe:
            loadedJson = json.load(aboutMe)
    elif Load == "project":
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("Projects"))) as aboutMe:
            loadedJson = json.load(aboutMe)
    else: 
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("limitedshell"))) as aboutMe:
            loadedJson = json.load(aboutMe)
    return loadedJson

def getUserInput(text):
    UserInput = input(text)
    return UserInput

def showresult(text):
    print(text)

def Execute(FullCommand, sites, passwords, passworddict):
    Command = FullCommand.split(" ")[0]
    if Command in LimitedJSONInfo().get("availableCommands"):
        if Command == "echo":
            return(" ".join(FullCommand.split(" ")[1:]))
        elif Command == "cat":
            if len(FullCommand.strip().split(" ")) == 2: 
                if FullCommand.strip().split(" ")[1].split(".")[0] == "passwords":
                    return (passwords)
                if LimitedJSONInfo().get("commands").get(FullCommand.strip().split(" ")[1]) is not None:
                    return(LimitedJSONInfo().get("commands").get(FullCommand.strip().split(" ")[1]))
                return ("cat: %s: No such file or directory"%(FullCommand.strip().split(" ")[1]))
        elif Command == 'dig' or Command == 'nslookup':
            if len(FullCommand.strip().split(" ")) == 2: 
                return(LimitedJSONInfo().get("commands").get(FullCommand.strip().split(" ")[1].split(".")[0] + Command))
        elif Command == 'msfvenom':
            if len(FullCommand.strip().split(" ")) == 2: 
                return(LimitedJSONInfo().get("commands").get(FullCommand.strip().split(" ")[1].split(".")[0] + Command))
        elif Command == 'ssh':
            if len(FullCommand.strip().split(" ")) == 2: 
               #print(sites)
                if FullCommand.strip().split(" ")[1].split(".")[0].split("@")[1] in sites:
                    #---- needs to be changed to prompt for js web implementation ----
                    tries = 0
                    while tries < 3:
                        remotepassword = getUserInput("garfield@%s Password: "%(FullCommand.strip().split(" ")[1]))
                        #print(passworddict.get(FullCommand.strip().split(" ")[1].split(".")[0].split("@")[1]))
                        if passworddict.get(FullCommand.strip().split(" ")[1].split(".")[0].split("@")[1]) == remotepassword:
                            showresult("connected to " + FullCommand.strip().split(" ")[1].split(".")[0].split("@")[1])
                            inssh = True
                            Site = FullCommand.strip().split(" ")[1].split(".")[0].split("@")[1]
                            return [Site, inssh]
                        tries +=1
        elif Command == 'help':
            return(LimitedJSONInfo().get("availableCommands").strip("[]").replace("'","").replace(",", "\n"))
        elif Command == 'exit':
            gamerun = False
            return ["Shutting down", gamerun, "exit"]
        else: 
            if len(FullCommand.strip().split(" ")) == 1:  
                return(LimitedJSONInfo().get("commands").get(Command))

def sshConnection(FullCommand, site):
    #print(site)
    command = FullCommand.split(" ")[0]

    if command in LimitedJSONInfo().get("availableCommands"):
        if command == "echo":
            return(" ".join(FullCommand.split(" ")[1:]))
        elif command == 'exit':
            inssh = False
            return ["Connection shutdown by user", inssh]
        elif command in ['pwd', 'sudo', 'whoami']:
            return(LimitedJSONInfo().get("commands").get(Command))
        elif command == "cat":
            if len(FullCommand.strip().split(" ")) == 2:  
                if LimitedJSONInfo().get('commands').get(site + FullCommand.strip().split(" ")[1]) is not None:
                    return(LimitedJSONInfo().get('commands').get(site + FullCommand.strip().split(" ")[1]))
                return ("cat: %s: No such file or directory"%(FullCommand.strip().split(" ")[1])) 
        else:
            if len(FullCommand.strip().split(" ")) == 1:  
                #print("Command", LimitedJSONInfo().get("commands").get(site + command))
                return(LimitedJSONInfo().get("commands").get(site + command))

def generatePasswords(sites):
    passwords = LimitedJSONInfo().get("commands").get("passwords.txt")
    passworddict = {}
    for x in sites:
        randomPassword = ''.join(random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(random.randint(8,15)))
        passwords = passwords.replace(x+"Password", randomPassword)
        passworddict.update({x:randomPassword})
    return passwords, passworddict

def generatePasswordshtml():
    passwords, passwordict = generatePasswords(["credentials", "aboutme", "projects"])
    LimitedShellCommands = LimitedJSONInfo()
    LimitedShellCommands.get("commands").update({"passwords.txt":passwords})
    writetoJson(LimitedShellCommands)
    updateShellJson()

def terminaltestrun():
    inssh = False
    sites = ["credentials", "aboutme", "projects"]
    Site = ""
    gamerun = True
    passwords, passworddict = generatePasswords(sites)
    while gamerun:
        usercommand = getUserInput("[garfield@garfieldPortfolio]-[~]$")
        output = Execute(usercommand, sites, passwords, passworddict)
        #print(inssh)
        if output is not None: 
            if len(output) == 2:
                inssh = output[1]
                while inssh:
                    site = output[0]
                    #print("Site", output)
                    remoteCommand = getUserInput("[garfield@%s]-[~]$"%(site))
                    SShOutput = sshConnection(remoteCommand, site)
                    if SShOutput is not None:
                        if len(SShOutput) == 2:
                            inssh = SShOutput[1]
                            showresult(SShOutput[0])
                        else:
                            showresult(SShOutput)
                    else:
                        showresult("bash: %s: Command not found"%(remoteCommand))
            elif len(output) == 3:
                gamerun = output[1]
                showresult(output[0])
                return output[0]
            else:
                showresult(output)
        else:
            showresult("bash: %s: Command not found"%(usercommand))

    showresult()

def updateShellJson():
    getProjects()
    getCertificates()
    aboutMe()


def aboutMe():
    AboutMe = LimitedJSONInfo("about")
    LimitedShellCommands = LimitedJSONInfo()
    Name = AboutMe.get("aboutMe").get("Name")
    Profession = AboutMe.get("aboutMe").get("PositionTitle")
    LimitedShellCommands.get("commands").update({"aboutmename.txt":"Name: " + Name})
    LimitedShellCommands.get("commands").update({"aboutmeprofession.txt":"Profession: "+ Profession})
    for x in AboutMe.get("ContactInfo").keys():
        contact = x + " : " + AboutMe.get("ContactInfo").get(x)
        if contact not in LimitedShellCommands.get("commands").get("aboutmecontact.txt"):
            LimitedShellCommands.get("commands").update({"aboutmecontact.txt": LimitedShellCommands.get("commands").get("aboutmecontact.txt") + contact + " \n "})
    writetoJson(LimitedShellCommands)



def getProjects():
    ProjectList = LimitedJSONInfo("project").get("Projects")
    LimitedShellCommands = LimitedJSONInfo()
    for x in ProjectList:
        ProjectName = x.get("Name").replace(" ", "")
        description = x.get("information")
        projectLink = x.get("Link")
        if ProjectName not in LimitedShellCommands.get("commands").get("projectsls"):
            LimitedShellCommands.get("commands").update({"projectsls": LimitedShellCommands.get("commands").get("projectsls") + ProjectName + ".txt \t "})
        LimitedShellCommands.get("commands").update({"projects" + ProjectName + ".txt": description + " \n " + projectLink})
    writetoJson(LimitedShellCommands)

def getCertificates():
    CertificationList = LimitedJSONInfo("about").get("aboutMe").get("Certifications")
    LimitedShellCommands = LimitedJSONInfo()
    for x in CertificationList.keys():
        CertifcationName = x.replace(" ", "_")
        CertificationExpiration = CertificationList.get(x)[CertificationList.get(x).index("Exp: "): CertificationList.get(x).index("Exp: ")+12]
        CertificationDescription = CertificationList.get(x)[CertificationList.get(x).index("Exp: ") +13:]
        if CertifcationName not in LimitedShellCommands.get("commands").get("credentialsls"):
            LimitedShellCommands.get("commands").update({"credentialsls":LimitedShellCommands.get("commands").get("credentialls") + CertifcationName+".txt \t "})
        LimitedShellCommands.get("commands").update({"credentials" + CertifcationName+".txt":CertificationExpiration + "\n" +CertificationDescription})
    writetoJson(LimitedShellCommands)


def writetoJson(datadict):
    serverCredentials = getJsonInformation()
    with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("limitedshell")), "w") as aboutMe:
        loadedJson = json.dump(datadict, aboutMe, indent=4)

if __name__ == "__main__":
    updateShellJson()
    terminaltestrun()