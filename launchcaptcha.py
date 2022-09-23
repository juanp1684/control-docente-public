import time
import winsound 
import random
from threading import Thread
from uicaptcha import UICaptcha
from datarequests import DataRequests

class LaunchCaptcha:

	def __init__(self, wait_time, class_duration,codsis, schedule_id, cookie):
		self.wait_time = wait_time
		self.class_duration = class_duration
		self.codsis = codsis
		self.schedule_id = schedule_id
		self.cookie = cookie

	def start(self):
		random_threshold = self.class_duration // 3
		first_wait_time = self.wait_time + random.randint(1, random_threshold)
		second_wait_time = self.wait_time + self.class_duration - random.randint(1, random_threshold)

		first_control = Thread(target=lambda: self.alarm(first_wait_time))
		second_control = Thread(target=lambda: self.alarm(second_wait_time))
		first_control.daemon = True
		second_control.daemon = True
		first_control.start()
		second_control.start()
		
	
	def alarm(self, time_until_control):

		time.sleep(time_until_control) 

		winsound.PlaySound("sound.wav", winsound.SND_ASYNC)
		
		codsis = self.codsis
		schedule_id = self.schedule_id

		uiCaptcha = UICaptcha()
		uiCaptcha.mainloop()
		data = codsis + ";" + str(schedule_id) + ";" + uiCaptcha.getResult()

		dataRequests = DataRequests()
		dataRequests.requestsPost(dataRequests.createReport(data), self.cookie)
