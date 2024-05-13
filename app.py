from bottle import *
from werkzeug.utils import secure_filename
import os
from aboutMe import *
from search import *
from Captcha import *
from googleEmail import *

@route('/')
def home():
    data_dict = aboutMeFun()
    return template("HTML/index.tpl", data_dict)

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


@route("/project")
def Projects():
    data_dict = aboutMeFun()
    data_dict_2 = template_dict()
    data_dict.update(data_dict_2)
    return template("HTML/project.tpl", data_dict)

#@route("/contact")
def Contact():
    data_dict = aboutMeFun()
    data_dict2 = captchaDict()
    data_dict.update(data_dict2)
    return template("HTML/contact.tpl", data_dict)

#@post("/contacted")
def Contacted():
    usernamebot = request.forms.get("username")
    Captcha = request.forms.get("Captcha")
    captchatext2 = request.forms.get("capt")
    if usernamebot != "N0":
        print("Bot")
    else:
        print("cap",Captcha)
        print("text",captchatext2)
        if Captcha == captchatext2:
            client_ip = request.environ.get('REMOTE_ADDR')
            try:
                remove_captcha("./Images/" + client_ip.replace(".","") +'captcha.png')
            except OSError as e:
                print(e)
            Subject = request.forms.get("subject")
            Email = request.forms.get("email")
            Message = request.forms.get("Message")
            sendEmail(Subject+Email, Message, "orangegarfieldspam01@gmail.com")
            print("hello",Subject)
            print("hello2", Email)
            print("hello3", Message)
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
#application = default_app()
run(host=data.get("Server").get("Address")[0:data.get("Server").get("Address").find(":")], port=os.environ.get('PORT', 5000), debug=True) 
