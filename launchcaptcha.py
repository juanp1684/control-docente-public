import datetime 
import time 
import winsound 
from threading import *
from uicaptcha import UICaptcha
from datarequests import DataRequests

class LaunchCaptcha:

	def __init__(self, launchTime):
		self.launchTime = launchTime

	def start(self):
		threadLaunch = Thread(target=self.alarm)
		threadLaunch.start()
	
	def alarm(self): 
		
		while True:
			time.sleep(1)
			
			currentTime = datetime.datetime.now().strftime("%H:%M:%S")
			print(currentTime, self.launchTime)
			
			if currentTime == self.launchTime:
				print("Lanza el captcha")
				winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
				
				codeSis = "2222"
				schudleId = 10

				uiCaptcha = UICaptcha()
				uiCaptcha.mainloop()
				data = codeSis + ";" + str(schudleId) + ";" + uiCaptcha.getResult()
				print(data)
				dataRequests = DataRequests()
				dataRequests.requestsPost(dataRequests.createReport(data))

				break

launchTime = "22:21:05"
launchCaptcha = LaunchCaptcha(launchTime)
launchCaptcha.start()