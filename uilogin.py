from tkinter import *
import os
from tkinter import messagebox
from datarequests import DataRequests

USER_PATH = os.path.expanduser('~')
APP_FOLDER_PATH	= USER_PATH + '/.control docente/'
SESSION_FILE_PATH = APP_FOLDER_PATH + 'session'
ALERT_TITLE = "Control docente"
SUCCES_MESSAGE = "Inicio de sesion exitoso"

class UILogin(Tk):
	logged_codsis = None
	logged_cookie = None
	
	def __init__(self):
		
		super().__init__()

		self.title("Login")
		self.geometry("320x220")
		self.resizable(0, 0)
		self.eval('tk::PlaceWindow . center')

		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=3)

		self.createWidgets()

	def createWidgets(self):

		self.sisCode = StringVar()
		self.password = StringVar()
		self.message = StringVar()

		labelSIS = Label(self, pady=5, text="Código SIS:")
		labelSIS.pack()

		inputSIS = Entry(self, textvariable=self.sisCode, font="Helvetica 20", justify=CENTER)
		inputSIS.pack()
		inputSIS.focus_set()

		labelPassword = Label(self, pady=5, text="Password:")
		labelPassword.pack()

		inputPassword = Entry(self, textvariable=self.password, show="*", font="Helvetica 20", justify=CENTER)
		inputPassword.pack()

		labelMessage = Label(self, pady=10, textvariable=self.message, font="14")
		labelMessage.pack()

		buttonLogin = Button(self, width=19, pady=5, text="Login", font="Helvetica 10", command=self.verifyValues)
		buttonLogin.pack()

	def register_cookie(self, response):
		session_file = open(SESSION_FILE_PATH, 'w+')
		self.logged_cookie = response.cookies
		cookie = self.logged_cookie.get('jwt')
		session_file.write(f'{self.logged_codsis}\n{cookie}')
		session_file.close()

	def verifyValues(self):
		if self.sisCode.get() == "" or self.password.get() == "":
			self.message.set("Llene los campos vacíos")
		else:
			requests_service = DataRequests()
			login_attempt = requests_service.requests_login_post(f'{{"codsis": "{self.sisCode.get()}", "password": "{self.password.get()}"}}')
			if login_attempt.status_code == 200:
				self.logged_codsis = self.sisCode.get()
				self.register_cookie(login_attempt)
				messagebox.showerror(ALERT_TITLE, SUCCES_MESSAGE)
				self.destroy()
			else:
				self.message.set("Código SIS y/o contraseña incorrectos")
