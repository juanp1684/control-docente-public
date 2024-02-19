from tkinter import messagebox
from captchamanagement import Captcha, CAPTCHA_PATH
from tkinter import Tk, StringVar, Canvas, PhotoImage, CENTER, Entry, Label, Button

ALERT_TITLE = 'Control'
SUCCES_MESSAGE = "Confirmado"
FAILED_MESSAGE = "Se excedio el maximo de intentos"

class UICaptcha(Tk):

	def __init__(self):

		super().__init__()

		self.WINDOW_WIDTH = 320
		self.WINDOW_HEIGTH = 210
		self.NUMBER_ATTEMPS = 3
		self.DURATION = 30000

		self.title("Captcha")
		self.geometry(str(self.WINDOW_WIDTH) + "x" + str(self.WINDOW_HEIGTH))
		self.iconbitmap("umss.ico")
		self.resizable(0, 0)
		self.wm_attributes("-topmost", True)
		self.protocol("WM_DELETE_WINDOW", lambda: None)

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

		self.cancel_autoclose_id = self.after(self.DURATION, self.destroy)

	def generateCaptcha(self):
		captcha = Captcha()
		captcha.generate()
		return str(captcha.getText())

	def verifyCaptcha(self):
		self.numberAttemps += 1
		if self.numberAttemps <= self.NUMBER_ATTEMPS:
			if self.valueTextCaptcha == self.textCaptcha.get():
				self.status = "completado"
				self.message.set("Texto correcto {}" . format(self.textCaptcha.get()))
				messagebox.showinfo(ALERT_TITLE, SUCCES_MESSAGE)
				self.destroy()
				return None
			
			self.status = "fallido"
			self.message.set("Texto incorrecto {}" . format(self.textCaptcha.get()))
			self.after_cancel(self.cancel_autoclose_id)
			self.cancel_autoclose_id = self.after(self.DURATION, self.destroy)

			if self.numberAttemps == self.NUMBER_ATTEMPS:
				messagebox.showinfo(ALERT_TITLE, FAILED_MESSAGE)
				self.destroy()
				return None
	
	def getResult(self):
		return str(self.numberAttemps) + ";" + self.status
