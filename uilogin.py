from tkinter import *

import tkinter as tk

class UILogin(tk.Tk):
	
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

	def verifyValues(self):
		if self.sisCode.get() == "" or self.password.get() == "":
			self.message.set("Llene los campos vacíos")
		else:
			if self.sisCode.get() == "abc" and self.password.get() == "123":
				self.message.set("Autenticación exitosa")
			else:
				self.message.set("Código SIS y/o contraseña incorrectos")

#guiUILogin = UILogin()
#guiUILogin.mainloop()