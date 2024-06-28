from bottle import *
from werkzeug.utils import secure_filename
import os
from aboutMe import *
from search import *
from Captcha import *
from credentials import *
from googleEmail import *
from PreviousJobs import *
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
    return template("HTML/index.tpl", data_dict)

@route("/gmailset")
def setgmail():
    auth_url = gmail_set()
    print(auth_url)
    return '''<meta http-equiv="refresh" content="0; URL="'''+ auth_url + '''" />''' 

@route("/iplogger")
def ipLogger():
    get_pretty()
    ipInfoJson, baseDirectory = IPJsonInfo()
    csv_location = os.path.join(baseDirectory, ipInfoJson.get("IP_CSV_File"))
    csvfile_dataframe = pandas.read_csv(csv_location)
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
    authurl = gmail_set()
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
    data_dict2 = captchaDict()
    data_dict.update(data_dict2)
    return template("HTML/contact.tpl", data_dict)

@post("/contacted")
def Contacted():
    data_dict2 = captchaDict()
    recaptcha_response = request.forms.get('g-recaptcha-response')
    payload = {
        'secret': data_dict2.get("Secret"),
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()

    if result.get('success'):
        email = request.forms.get("email")
        subject = request.forms.get("subject")
        message = request.forms.get("Message")
        gmail_send_message(subject, message, email)
    else:
        print("----- BOT ACCESSED ----")
        return '''<meta http-equiv="refresh" content="0; URL='./'" />''' 

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
    print(client_ip2)
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
if localhost.upper() == "TRUE":
    run(host=data.get("Server").get("Address")[0:data.get("Server").get("Address").find(":")], port=os.environ.get('PORT', 5000), debug=True) 
else:
    application = default_app()
