from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from AdvancedFernetDataEncryption import *
from inspect import getcallargs
import json, smtplib, ssl

def getJsonInformation(Version = ""):
    if "me" in Version.lower():
        with open("./information/about-me.json") as aboutMe:
            loadedJson = json.load(aboutMe)
    else:
        with open("./information/credentials.json") as Credentials:
            loadedJson = json.load(Credentials)
    return loadedJson

def makeInformationPretty():
    aboutMeJson = getJsonInformation("me")
    certification_dict = aboutMeJson.get("aboutMe").get("Certifications")
    skills_dict = aboutMeJson.get("aboutMe").get("Skills")
    certification_result = ""
    for key, values in certification_dict.items():
        certification_result = certification_result + ('''
        <p>%s</p> <p>%s</p> <br>
        ''' %(key, values))

    skills_result = ""
    for key, values in skills_dict.items():
        skills_result = skills_result + ('''
        <p>%s</p> <progress value=%s max="100"></progress> <br>
        ''' %(key, values))
    return skills_result, certification_result

def aboutMeFun():
    skills_result, certification_result = makeInformationPretty()
    aboutMeInformation = getJsonInformation("me")
    aboutMe_dict = {"firstName": aboutMeInformation.get("aboutMe").get("Name").split(" ")[0],
    "fullName": aboutMeInformation.get("aboutMe").get("Name"), 
    "majorName": aboutMeInformation.get("aboutMe").get("Major"),
    "schoolName": aboutMeInformation.get("aboutMe").get("School"),
    "positionTitle": aboutMeInformation.get("aboutMe").get("PositionTitle"), 
    "certifications": certification_result, #Ditectiona "Name of cert": date
    "skills": skills_result, #Dictionary "Name of skill": "percentage"
    "email": aboutMeInformation.get("ContactInfo").get("email"), 
    "githubLink": aboutMeInformation.get("ContactInfo").get("Github")}
    return aboutMe_dict

def listtoString(list):
    finalstring = ""
    for x in range(len(list)-1):
        finalstring += list[x] + ", "
    finalstring += list[len(list)-1]
    return finalstring

def sendEmail(subject, message, Email):
    data = getJsonInformation()
    server = smtplib.SMTP("smtp.gmail.com", 587 )  ## This will start our email server
    server.starttls(context=ssl.create_default_context())         ## Starting the server
    #---- Gets the credentials for the gmail login ----
    server.login(data.get("email"), dataDecryption(data.get("EmailPassword")))
    mimeMessage = MIMEMultipart()
    #---- Send a message witha certain subject ----
    mimeMessage['to'] = Email
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(message, 'plain'))
    server.sendmail(data.get("email"), Email, mimeMessage.as_string())
    server.quit()