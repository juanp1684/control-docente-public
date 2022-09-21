from captcha.image import ImageCaptcha
import os
import random
import string

USER_PATH = os.path.expanduser('~')
APP_FOLDER_PATH	= USER_PATH + '/.control docente/'
CAPTCHA_PATH = APP_FOLDER_PATH + "captcha.png"
CAPTCHA_LENGHT = 5

class Captcha:

	def __init__(self):
		self.captchaText = ""
	
	def generate(self):
		image = ImageCaptcha(width = 250, height = 80, fonts=['arial.ttf'])

		self.captchaText = "".join(random.choice(string.digits) for _ in range(CAPTCHA_LENGHT))

		if not os.path.isdir(APP_FOLDER_PATH):
			os.makedirs(APP_FOLDER_PATH)

		image.write(self.captchaText, CAPTCHA_PATH)

	def getText(self):
		return self.captchaText
