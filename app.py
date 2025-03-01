from bottle import *
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from aboutMe import *
from search import *
from Captcha import *
from credentials import *
from googleEmail import *
from PreviousJobs import *
from limitedshell import generatePasswordshtml
from ip_logger import *
import requests,json
import pandas

@route('/')
def home():
    client_ip = request.environ.get('REMOTE_ADDR')
    client_ip2 = request.environ.get('HTTP_X_FORWARDED_FOR')
    print(client_ip2)
    ip_logged(client_ip, client_ip2)
    data_dict = aboutMeFun()
    data_dict2 = MakeJobs()
    data_dict.update(data_dict2)
    #if request.get_cookie("SessionID") is not None:
    #    os.remove(captchavalues.get(sessionID+"path"))
    return template("HTML/index.tpl", data_dict)

@route("/sshpassword")
def sshgenpassword():
    generatePasswordshtml()
    return '''<meta http-equiv="refresh" content="0; URL='./'" />''' 

@route("/gmailset")
def setgmail():
    auth_url = "./"
    #print(auth_url)
    return '''<meta http-equiv="refresh" content="0; URL="'''+ auth_url + '''" />''' 

@route("/iplogger")
def ipLogger():
    get_pretty()
    ipInfoJson, baseDirectory = IPJsonInfo()
    csv_location = os.path.join(baseDirectory, ipInfoJson.get("IP_CSV_File"))
    csvfile_dataframe = pandas.read_csv(csv_location)
    print("html")
    print(csvfile_dataframe.to_html())
    return csvfile_dataframe.to_html()

@route("/robots.txt")
def robots():
    return static_file("robots.txt", root=os.path.abspath('SEO'))

@route("/about-me")
def aboutMe():
    data_dict = aboutMeFun()
    return template("HTML/about-me.tpl", data_dict)

@post("/SearchProject")
def searchedProjects():
    searchquery = request.forms.get("SearchBox")
    queried_list = search(searchquery)
    data_dict = aboutMeFun()
    data_dict_2 = template_dict(queried_list)
    data_dict.update(data_dict_2)
    return template("HTML/project.tpl", data_dict)

@route("/SearchProject/<query>")
def searchqueryProject(query):
    queried_list = search(query)
    data_dict = aboutMeFun()
    data_dict_2 = template_dict(queried_list)
    data_dict.update(data_dict_2)
    return template("HTML/project.tpl", data_dict)

@route("/gmailapi")
def gmailapi():
    #authurl = gmail_set()
    return '''<meta http-equiv="refresh" content="0; URL='./'" />''' 

@route("/project")
def Projects():
    data_dict = aboutMeFun()
    data_dict_2 = template_dict()
    data_dict.update(data_dict_2)
    return template("HTML/project.tpl", data_dict)

@route("/contact")
def Contact():
    data_dict = aboutMeFun()
    gcpatcha = data.get("Server").get("googlecaptcha")
    if gcpatcha == "True":
        data_dict2 = googlecaptcha()
    else:
        sessionToken, data_dict2 = normalcaptcha()
        response.set_cookie("SessionID", sessionToken, expires=time.mktime((datetime.now() + timedelta(hours=1)).timetuple()))
    data_dict.update(data_dict2)
    return template("HTML/contact.tpl", data_dict)

@post("/contacted")
def Contacted():
    gcpatcha = data.get("Server").get("googlecaptcha")
    if gcpatcha == "True":
        recaptcha_response = request.forms.get('g-recaptcha-response')
        result = getgooglecaptcharesults(recaptcha_response)
    else:
        recaptcha_response = request.forms.get('gcaptcha')
        result = checkcaptcha(recaptcha_response, request.get_cookie("SessionID"))
    # {'success': False, 'error-codes': ['invalid-input-response']}

    if result.get('success'):
        email = request.forms.get("email")
        subject = request.forms.get("subject")
        message = request.forms.get("Message")
        gmail = data.get("Server").get("gmail")
        if gmail == "True":
            gmail_send_message(subject, message, email)
        else:
            send_email(subject, message, email)
        return '''<meta http-equiv="refresh" content="0; URL='./project'" />''' 
    else:
        client_ip2 = request.environ.get('HTTP_X_FORWARDED_FOR')
        blacklist(client_ip2)
        print("----- BOT ACCESSED ----")
        print("----- Blacklist ip addr: %s -----"%(client_ip2))
        return '''<meta http-equiv="refresh" content="0; URL='./contact'" />''' 

@route("/information/<filename>")
def informationfile(filename):
    return static_file(filename, root=os.path.abspath('information'))

@route('/HTML/<filename>')
def server_HTML(filename):
    #---- Returns the static file for all HTML files used ----
    return static_file(filename, root=os.path.abspath('HTML'))

@route('/Images/<filename>')
def server_Images(filename):
    #---- RReturns the static file for all Images used ----
    return static_file(filename, root=os.path.abspath('Images'))

@route('/Scripts/<filename>')
def server_Scripts(filename):
    #---- Returns the static file for all Scripts used ----
    return static_file(filename, root=os.path.abspath('Scripts'))

@error(404)
def error404(error):
    print("404", error)
    client_ip2 = request.environ.get('HTTP_X_FORWARDED_FOR')
    blacklist(client_ip2)
    print("----- Blacklist ip addr: %s -----"%(client_ip2))
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@error(303)
def error303(error):
    print("303", error)
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

@error(500)
def error500(error):
    print("500", error)
    return '''<meta http-equiv="refresh" content="0; URL='./'" />'''

#---- Top one is for heroku or cloud based hosting ----
data = getJsonInformation()
localhost = data.get("Server").get("localhost")
run(host=data.get("Server").get("Address")[0:data.get("Server").get("Address").find(":")], port=os.environ.get('PORT', 5000), debug=True) 
