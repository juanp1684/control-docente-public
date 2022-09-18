from captcha.image import ImageCaptcha
import os
import random

USER_PATH = os.path.expanduser('~')
APP_FOLDER_PATH	= USER_PATH + '/.control docente/'
CAPTCHA_PATH = APP_FOLDER_PATH + "captcha.png"

class Captcha:

	def __init__(self):
		self.captchaText = ""
	
	def generate(self):
		image = ImageCaptcha(width = 250, height = 80, fonts=['C:/Windows/Fonts/Arial.ttf'])

		for number in range(5):
			digit = random.randint(0, 9)
			self.captchaText += str(digit)
		
		if not os.path.isdir(APP_FOLDER_PATH):
			os.makedirs(APP_FOLDER_PATH)

		data = image.generate(self.captchaText)
		image.write(self.captchaText, CAPTCHA_PATH)

	def getText(self):
		return self.captchaText
