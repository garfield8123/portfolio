from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from AdvancedFernetDataEncryption import *
from inspect import getcallargs
import json, smtplib, ssl
from credentials import *

def getAboutMe(Version = ""):
    serverCredentials = getJsonInformation()
    if "me" in Version.lower():
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("AboutMe"))) as aboutMe:
            loadedJson = json.load(aboutMe)
    elif "site" in Version.lower():
        with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("Site-Template"))) as siteTemplate:
            loadedJson = json.load(siteTemplate)
    return loadedJson

def makeInformationPretty():
    aboutMeJson = getAboutMe("me")
    siteTemplateJson = getAboutMe("site")
    certification_dict = aboutMeJson.get("aboutMe").get("Certifications")
    skills_dict = aboutMeJson.get("aboutMe").get("Skills")

    skillStyle = siteTemplateJson.get("Skills")
    if certification_dict is not None:
        certification_result = siteTemplateJson.get("Certifications start").replace("%title", "Certifications")
        for key, values in certification_dict.items():
            certificateStyle = siteTemplateJson.get("Certifications")
            certificateStyle = certificateStyle.replace("%name", key)
            certificateStyle = certificateStyle.replace('%expire', values)
            certification_result = certification_result + certificateStyle
    else:
        education_dict = aboutMeJson.get("aboutMe").get("Education")
        certification_result = siteTemplateJson.get("Certifications start").replace("%title", "Education")
        for key, values in education_dict.items():
            certificateStyle = siteTemplateJson.get("Certifications")
            certificateStyle = certificateStyle.replace("%name", key)
            certificateStyle = certificateStyle.replace('%expire', values)
            certification_result = certification_result + certificateStyle


    skills_result = siteTemplateJson.get("Skills start")
    for key, values in skills_dict.items():
        skillStyle = skillStyle.replace("%name", key)
        skillStyle = skillStyle.replace("%value",values)
        skills_result = skills_result + skillStyle
    certification_result = certification_result + siteTemplateJson.get("Certifications end")
    skills_result = skills_result + siteTemplateJson.get("Skills end")
    return skills_result, certification_result

def aboutMeFun():
    skills_result, certification_result = makeInformationPretty()
    aboutMeInformation = getAboutMe("me")
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