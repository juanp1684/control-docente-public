from turtle import width
from captchamanagement import Captcha, CAPTCHA_PATH
from tkinter import *
from PIL import Image, ImageTk

import tkinter as tk

class UICaptcha(tk.Tk):

	def __init__(self):

		super().__init__()

		self.WINDOW_WIDTH = 320
		self.WINDOW_HEIGTH = 210
		self.NUMBER_ATTEMPS = 3
		self.SECONDS = 30000

		self.title("Captcha")
		self.geometry(str(self.WINDOW_WIDTH) + "x" + str(self.WINDOW_HEIGTH))
		self.iconbitmap("umss.ico")
		self.resizable(0, 0)
		self.eval('tk::PlaceWindow . center')
		self.wm_attributes("-topmost", True)

		self.valueTextCaptcha = self.generateCaptcha()
		self.numberAttemps = 0
		self.status = "omision"
		
		self.createWidgets()

	def createWidgets(self):
		self.message = StringVar()
		self.textCaptcha = StringVar()

		self.canvas = Canvas(self, width=300, height=80)
		self.canvas.pack()
		self.imageCaptcha = PhotoImage(file=CAPTCHA_PATH)
		self.canvas.create_image(self.WINDOW_WIDTH/2, 40, anchor=CENTER, image=self.imageCaptcha)

		inputCaptcha = Entry(self, textvariable=self.textCaptcha, font="Helvetica 20", justify=CENTER)
		inputCaptcha.focus_set()
		inputCaptcha.pack()

		labelMessage = Label(self, pady=10, textvariable=self.message, font="14")
		labelMessage.pack()

		buttonVerify = Button(self, width=19, pady=5, text="Verificar", font="Helvetica 10", command=self.verifyCaptcha)
		buttonVerify.pack()

		self.after(self.SECONDS, lambda:self.destroy())

	def generateCaptcha(self):
		captcha = Captcha()
		captcha.generate()
		return str(captcha.getText())

	def verifyCaptcha(self):
		# print("Texto captha {}" . format(self.valueTextCaptcha))

		self.numberAttemps += 1
		# print("Intento número: {}" . format(self.numberAttemps))

		if self.numberAttemps <= self.NUMBER_ATTEMPS:
			if self.valueTextCaptcha == self.textCaptcha.get():
				self.status = "completado"
				self.message.set("Texto correcto {}" . format(self.textCaptcha.get()))
				# print("SON IGUALES")
				self.destroy()
				return None
			
			self.status = "fallido"
			self.message.set("Texto incorrecto {}" . format(self.textCaptcha.get()))
			# print("SON DIFERENTES")

			if self.numberAttemps == self.NUMBER_ATTEMPS:
				self.destroy()
				return None
	
	def getResult(self):
		return str(self.numberAttemps) + ";" + self.status

'''
guiCaptcha = UICaptcha()
guiCaptcha.mainloop()
print("\nRESULTADO: {}" . format(guiCaptcha.getResult()))
'''
