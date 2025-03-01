import os.path
import google.auth
import base64
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import json, smtplib, ssl

from AdvancedFernetDataEncryption import *
from credentials import *
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

serverCredentials = getJsonInformation()
gmail_oauth = os.getenv("GMAIL_Credential_Location")
token_File = os.getenv("Gmail_Token_Location")
email_credential = os.getenv("GMAIL_Credential_Location")
email_info = os.getenv("email_Location")

def gmail_set():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  auth_url = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_File):
    creds = Credentials.from_authorized_user_file(token_File, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          email_credential, SCOPES
      )
      auth_url, _ = flow.authorization_url(prompt='consent')
      print(f'Please go to this URL to authorize the application: {auth_url}')
      gmail_oauth_file = gmail_oauth
      if os.path.isfile(gmail_oauth_file):
        with open(gmail_oauth_file, 'r') as file:
          content =file.read()
        content = content.replace(content, "")
      with open(gmail_oauth_file, 'w') as file:
        file.write(auth_url)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_File, "w") as token:
      token.write(creds.to_json())
  return auth_url


def gmail_send_message(Subject, Message, Email):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  import json
  with open(email_info, 'r') as email:
    emaillist = json.load(email)
  with open(token_File, 'r') as token:
    creds_data = json.load(token)
  creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(Message)

    message["To"] = "orangegarfieldspam01@gmail.com"
    message["From"] =  Email
    message["Subject"] = Subject + "//" + Email

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

def send_email(Subject, Message, Email):
  server = smtplib.SMTP("smtp.gmail.com", 587 )  ## This will start our email server
  server.starttls(context=ssl.create_default_context())         ## Starting the server
  #---- Gets the credentials for the gmail login ----
  garfieldemail, password = email_credentials()
  server.login(garfieldemail, password)
  mimeMessage = MIMEMultipart()
  #---- Send a message witha certain subject ----
  mimeMessage['to'] = garfieldemail
  mimeMessage['subject'] = Subject + "From " + Email
  mimeMessage.attach(MIMEText(Message, 'plain'))
  server.sendmail(garfieldemail, garfieldemail, mimeMessage.as_string())
  server.quit()
  print(Subject)

def getemailcreds():
  with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("emailInfo"))) as emailInfo:
    loadedJson = json.load(emailInfo)
  return loadedJson

def email_credentials():
  emailjson = getemailcreds()
  data = getJsonInformation()
  encryption = data.get("Server").get("encryption")
  if encryption == "True":
    return dataDecryption(emailjson.get("email")), dataDecryption(emailjson.get("password"))
  else:
    return os.environ.get("EMAIL"), os.environ.get("EMAILPASSWORD")

def updateemailcreds(email, password):
  emailjson = getemailcreds()
  encryptedEmail = dataEncryption(email, 10, 20)
  encryptedPassword = dataEncryption(password, 10, 20)
  emailjson.update({"email":encryptedEmail, "password":encryptedPassword})
  with open(os.path.join(serverCredentials.get("Server Files").get("baseDirectory"), serverCredentials.get("Server Files").get("emailInfo")), "w") as emailInfo:
    loadedJson = json.dump(emailjson, emailInfo, indent=4)
  return "'"
  

if __name__ == "__main__":
  #gmail_set()
  send_email("testsubject", "test", "orangegarfieldspam01@gmail.com")