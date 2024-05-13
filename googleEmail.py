from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#from AdvancedFernetDataEncryption import *
from aboutMe import *

def sendEmail(subject, message, Email, debug=False):
    data = getJsonInformation()
    if debug:
        print("Email Subject: ", subject)
        print("Email To: ", Email)
        print("Email Message: ", message)
        print("Email From: ", dataDecryption(data.get("Email")))
        print("Email Password: ", dataDecryption(data.get("EmailPassword")))
    server = smtplib.SMTP("smtp.gmail.com", 587 )  ## This will start our email server
    server.starttls(context=ssl.create_default_context())         ## Starting the server
    #---- Gets the credentials for the gmail login ----
    server.login(dataDecryption(data.get("Email")), dataDecryption(data.get("EmailPassword")))
    mimeMessage = MIMEMultipart()
    #---- Send a message witha certain subject ----
    mimeMessage['to'] = Email
    mimeMessage['subject'] = subject
    mimeMessage.attach(MIMEText(message, 'plain'))
    server.sendmail(dataDecryption(data.get("Email")), Email, mimeMessage.as_string())
    server.quit()