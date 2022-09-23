import pystray
from PIL import Image
from datarequests import DataRequests
from launchcaptcha import LaunchCaptcha
from uilogin import UILogin
from datetime import datetime, timedelta, time
import time as thread_time
import os

RESPONSE_TIME_FORMAT = "%H:%M:%S"
RESPONSE_LAST_CONNECTION_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
USER_PATH = os.path.expanduser('~')
APP_FOLDER_PATH	= USER_PATH + '/.control docente/'
SESSION_FILE_PATH = APP_FOLDER_PATH + 'session'

def exit_application(icon, item):
	icon.stop()
	os._exit(0)

def start_tray_icon():
	image = Image.open('umss.ico')
	icon = pystray.Icon('control docente', image, menu=pystray.Menu(
		pystray.MenuItem("cerrar", exit_application)
		))
	icon.run_detached()

def parse_schedule_time (schedule_time):
	return datetime.strptime(schedule_time, RESPONSE_TIME_FORMAT)

def set_schedules_for_today(all_schedules, cookie):
	today_day = datetime.today().weekday()
	today_schedules = list(filter(lambda schedule: schedule['day_of_week'] == today_day, all_schedules))
	today_schedules = [{'start': parse_schedule_time(schedule['start_time']),
			'end': parse_schedule_time(schedule['end_time']),
			'id': schedule['id']} for schedule in today_schedules]
	today_schedules = list(filter(lambda schedule: schedule['start'].time() > datetime.now().time(), today_schedules))

	for schedule in today_schedules:
		wait = (schedule['start'] - datetime.now()).seconds
		duration = (schedule['end'] - schedule['start']).seconds
		class_control = LaunchCaptcha(wait, duration, codsis, schedule['id'], cookie)
		class_control.start()
	print("schedules set for the day")

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
	if not os.path.isdir(APP_FOLDER_PATH):
			os.makedirs(APP_FOLDER_PATH)

	if (os.path.exists(SESSION_FILE_PATH)):
		file = open(SESSION_FILE_PATH, 'r')
		data = file.read().split('\n')
		codsis = data[0]
		cookie = {'jwt': data[1]}
		file.close()
	else :
		guiUILogin = UILogin()
		guiUILogin.mainloop()
		codsis = guiUILogin.logged_codsis
		cookie = guiUILogin.logged_cookie
	request_manager = DataRequests()
	response_data = request_manager.requestGet(sisCode=codsis, cookie=cookie)
	all_schedules = response_data['schedules']
	last_connection = datetime.strptime( response_data['last_connection'], RESPONSE_LAST_CONNECTION_FORMAT)

	start_tray_icon()

	#TODO
	#send_catchup_reports(last_connection, cookie)

	while True:
		set_schedules_for_today(all_schedules, cookie)
		tomorrow = datetime.now() + timedelta(days=1)
		difference = (datetime.combine(tomorrow, time.min) - datetime.now()).seconds + 60 #just in case addition
		# print(difference)
		thread_time.sleep(difference)
		

	""" guiCaptcha = UICaptcha()
	guiCaptcha.mainloop()
	data = codeSis + ";" + str(schudleId) + ";" + guiCaptcha.getResult()
	print(data)
	dataRequests = DataRequests()
	dataRequests.requestsPost(dataRequests.createReport(data)) """
