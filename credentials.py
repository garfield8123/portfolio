import json
import os
import sys
import platform
import subprocess

def getJsonInformation(path = ""):
    with open(os.environ["SERVER_CREDENTIALS_PORTFOLIO"]) as Credentials:
        loadedJson = json.load(Credentials)
    return loadedJson

def getOS():
    os_name = platform.system()
    if os_name == 'Windows':
        return "Windows"
    else:
        return "Linux"

def crashError(set_google = ""):
    if set_google != "":
        print("Usage: python3 credentials.py SET/RM <PATH_TO_Credentials.json> <google_Site_key> <google_Secret_key>")
    else:
        print("Usage: python3 credentials.py SET/RM <PATH_TO_Credentials.json>")
    sys.exit(1)

def createSystemVariables(variableName, variableValue):
    if platform.system() == 'Windows':
        command = f'setx {variableName} "{variableValue}"'
        # Execute the command in the shell
        subprocess.run(command, shell=True)
    else:
        shell_profile = os.path.expanduser('~/.bashrc') 
        #if 'bash' in os.getenv('SHELL', '') else os.path.expanduser('~/.zshrc')
        command = f'\nexport {variableName}="{variableValue}"\n'
        with open(shell_profile, 'r') as file:
            lines = [line.strip() for line in file.readlines()]
        result = True
        for x in lines:
            print(command.strip() in x)
            if command.strip() in x:
                result = False
                exit
        if result:
            with open(shell_profile, 'a') as file:
                file.write(command)

def deleteSystemVariables(variableName, variableValue):
    if platform.system() == 'Windows':
        command = f'REG delete HKCU\\Environment /F /V {variableName}'
        subprocess.run(command, shell=True)
    else:
        shell_profile = os.path.expanduser('~/.bashrc') 
        #if 'bash' in os.getenv('SHELL', '') else os.path.expanduser('~/.zshrc')
        command = f'\nexport {variableName}="{variableValue}"\n'
        #shutil.copyfile(shell_profile, shell_profile + ".bak")
        result = ""
        with open(shell_profile, "r") as file:
            for line in file:
                if line.strip() in command.strip():
                    line = line.strip().replace(command.strip(), "")
                result += line
        with open(shell_profile, "w") as file:   
            file.write(result)

def setCaptchaKey():
    with open(os.environ["SERVER_CREDENTIALS_PORTFOLIO"], "r") as Credentials:
        loadedJson = json.load(Credentials)
    loadedJson.get("Captcha")["Site_key"] = os.environ["GOOGLE_SITE_KEY"]
    loadedJson.get("Captcha")["Secret_key"] = os.environ["GOOGLE_SECRET_KEY"]
    with open(os.environ["SERVER_CREDENTIALS_PORTFOLIO"], "w") as file:
        json.dump(loadedJson, file, indent=4)

def setLocalhost(Localhost):
    with open(os.environ["SERVER_CREDENTIALS_PORTFOLIO"], "r") as Credentials:
        loadedJson = json.load(Credentials)
    loadedJson.get("Server")["localhost"] = str(Localhost)
    with open(os.environ["SERVER_CREDENTIALS_PORTFOLIO"], "w") as file:
        json.dump(loadedJson, file, indent=4)


if __name__ == "__main__":
    localhost = input("Running localhost")
    runninglocalhost = False
    if localhost.strip().lower() in ['true', 'yes']:
        runninglocalhost = True
    if len(sys.argv) < 4:
        crashError()
    if sys.argv[1].upper() in ["SET", "RM"]:
        if "SET" == sys.argv[1].upper():
            createSystemVariables("SERVER_CREDENTIALS_PORTFOLIO", sys.argv[2])
            setLocalhost(runninglocalhost)
            if len(sys.argv) > 3:
                if len(sys.argv) != 5:
                    crashError("google")
                createSystemVariables("GOOGLE_SITE_KEY", sys.argv[3])
                createSystemVariables("GOOGLE_SECRET_KEY", sys.argv[4])
                setCaptchaKey()
            sys.exit(1)
        else:
            deleteSystemVariables("SERVER_CREDENTIALS_PORTFOLIO", sys.argv[2])
            if len(sys.argv) > 3:
                if len(sys.argv) != 5:
                    crashError("google")
                deleteSystemVariables("GOOGLE_SITE_KEY", sys.argv[3])
                deleteSystemVariables("GOOGLE_SECRET_KEY", sys.argv[4])
            sys.exit(1)
    else:
        crashError()
