
# Import the following modules
from bottle import *
from captcha.image import ImageCaptcha
import random,string,os, json, requests
from credentials import *
from AdvancedFernetDataEncryption import generateSessionToken
 
def create_captcha(width, height):
    
    captcha_text = ''.join(random.choice(string.digits) for _ in range(random.randint(4,8)))
    image = ImageCaptcha(width, height)
    # generate the image of the given text
    data = image.generate(captcha_text)  
    
    # write the image on the given file and save it
    word = randomword(15)
    captcha_path = "./Images/" + word +'captcha.png'
    image.write(captcha_text, "./Images/" + word +'captcha.png')
    
    #image.save("./Images/" + word +'captcha.png')
    return captcha_text, captcha_path

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def captchaDict():
    #captcha_text, captcha_path = create_captcha(350,100)
    credentials = getJsonInformation()
    site_key = os.getenv("Site_key")
    secret_key = os.getenv("Secret_key")
    return {'site_key':site_key, "Secret":secret_key} 

def remove_captcha(filename):
    os.remove(filename)

def googlecaptcha():
    captchacreds = captchaDict()
    #print(captchacreds.get("site_key"))
    return {"captchaHead":'<script src="https://www.google.com/recaptcha/enterprise.js?render='+captchacreds.get("site_key")+'"></script>',"captcha":'<div class="row"><div class="col-md-12"><div class="g-recaptcha" style="margin:0 auto; width:304px; height : 78px" data-sitekey="' + captchacreds.get("site_key") +'"></div></div></div>'}

def getgooglecaptcharesults(recaptcha_response):
    data_dict2 = captchaDict()
    payload = {
        'secret': data_dict2.get("Secret"),
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    return result

captchavalues = {}
def normalcaptcha():
    captchatext, captchapath = create_captcha(200, 50)
    sessionToken = randomword(20)
    captchavalues.update({sessionToken: captchatext, sessionToken+"path":captchapath})
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR')
    return sessionToken, {"captchaHead":'',"captcha":'<div class="row"> <div class="col-md-12"> <img src="' + captchapath + '"> <input type="text" id="gcaptcha" name="gcaptcha" placeholder="captcha" required></div></div>'}

def checkcaptcha(gcaptcha, sessionID):
    if gcaptcha == captchavalues.get(sessionID):
        os.remove(captchavalues.get(sessionID+"path"))
        return {'success': True, 'error-codes': ['invalid-input-response']}
    else:
        os.remove(captchavalues.get(sessionID+"path"))
        return {'success': False, 'error-codes': ['invalid-input-response']}