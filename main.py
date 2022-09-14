from datarequests import DataRequests
from uicaptcha import UICaptcha
from uilogin import UILogin
import random

if __name__ == "__main__":
	'''
	flag = random.randint(0, 1)
	print("Bandera es {}" . format(flag))
	if flag == 0:
		print("Mostrar ventana login")
		uiLogin = UILogin()
		uiLogin.mainloop()
		#Code SIS: 201800124
		data = DataRequests()
		data.requestGet("201800124")
	else:
		print("Mostrar ventana captcha")
		uiCaptcha = UICaptcha()
		uiCaptcha.mainloop()
	'''

	codeSis = "2222"
	schudleId = 2
	
	guiCaptcha = UICaptcha()
	guiCaptcha.mainloop()
	data = codeSis + ";" + str(schudleId) + ";" + guiCaptcha.getResult()
	print(data)
	dataRequests = DataRequests()
	dataRequests.requestsPost(dataRequests.createReport(data))