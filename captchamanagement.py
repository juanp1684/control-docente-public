from captcha.image import ImageCaptcha
import random

class Captcha:

	def __init__(self):
		self.captchaText = ""
	
	def generate(self):
		image = ImageCaptcha(width = 250, height = 80)

		for number in range(5):
			digit = random.randint(0, 9)
			self.captchaText += str(digit)

		data = image.generate(self.captchaText)
		
		image.write(self.captchaText, "captcha.png")

	def getText(self):
		return self.captchaText