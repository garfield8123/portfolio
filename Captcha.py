
# Import the following modules
from bottle import *
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random,string,os
 
def create_captcha(width, height):
    
    captcha_text = ''.join(random.choice(string.digits) for _ in range(random.randint(4,8)))
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    font = ImageFont.load_default()

    draw = ImageDraw.Draw(image)
    
    # Apply random rotation to each character
    for i, char in enumerate(captcha_text):
        char_image = Image.new('RGBA', (50, 50), (255, 255, 255, 0))
        char_draw = ImageDraw.Draw(char_image)
        char_draw.text((10, 10), char, (0, 0, 0), font=font)
        char_image = char_image.rotate(random.randint(-30, 30), expand=1)
        
        # Apply random distortion
        distorted_image = Image.new('RGBA', char_image.size)
        for x in range(char_image.width):
            for y in range(char_image.height):
                src_x = int(x + random.choice([-2, -1, 1, 2]))
                src_y = int(y + random.choice([-2, -1, 1, 2]))
                if 0 <= src_x < char_image.width and 0 <= src_y < char_image.height:
                    distorted_image.putpixel((x, y), char_image.getpixel((src_x, src_y)))
        
        image.paste(distorted_image, (i * 40 + 10, 10), distorted_image)
    
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    #image.show()
    client_ip = request.environ.get('REMOTE_ADDR')
    captcha_path = "./Images/" + client_ip.replace(".","") +'captcha.png'
    image.save("./Images/" + client_ip.replace(".","") +'captcha.png')
    return captcha_text, captcha_path

def captchaDict():
    captcha_text, captcha_path = create_captcha(350,100)

    return {'CaptchaPath':captcha_path, "captcha":captcha_text} 

def remove_captcha(filename):
    os.remove(filename)

