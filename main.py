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
REPORT_DATA_FORMAT = '{};{};{};{}'

def report_skipped_schedules(schedules, cookie, codsis):
	request_manager = DataRequests()
	for schedule in schedules:
		request_manager.requestsPost(request_manager.createReport(REPORT_DATA_FORMAT.format(codsis, schedule['id'], 0, 'omision')), cookie)

def days_in_between(last_day):
	today = datetime.now()
	result = []
	day_in_between = last_day + timedelta(days=1)
	while day_in_between.date() < today.date():
		result.append(day_in_between.weekday())
		day_in_between = day_in_between + timedelta(days=1)
	return result

def send_catchup_reports(last_date, cookie, schedules, codsis):
	last_day_of_week = last_date.weekday()
	days_difference = (datetime.now() - last_date).days
	today_day = datetime.now().weekday()
	schedules = [{'start': parse_schedule_time(schedule['start_time']),
			'id': schedule['id'],
			'day_of_week': schedule['day_of_week']} for schedule in schedules]
	if last_day_of_week == today_day and days_difference == 0: #both dates within the same day
		today_schedules = list(filter(lambda schedule: schedule['day_of_week'] == today_day, schedules))
		today_schedules = list(filter(lambda schedule: schedule['start'].time() < datetime.now().time() and 
							schedule['start'].time() > last_date.time(), today_schedules))
		report_skipped_schedules(today_schedules, cookie, codsis)
	else:
		total_missed_schedules = list(filter(lambda schedule: schedule['day_of_week'] == last_day_of_week, schedules))
		total_missed_schedules = list(filter(lambda schedule: schedule['start'].time() > last_date.time(), total_missed_schedules))

		today_missed_schedules = list(filter(lambda schedule: schedule['day_of_week'] == today_day, schedules))
		today_missed_schedules = list(filter(lambda schedule: schedule['start'].time() < datetime.now().time(), today_missed_schedules))
		total_missed_schedules.extend(today_missed_schedules)
		
		days_to_add = days_in_between(last_date)
		for day in days_to_add:
			day_schedules = list(filter(lambda schedule: schedule['day_of_week'] == day, schedules))
			total_missed_schedules.extend(day_schedules)		
		report_skipped_schedules(total_missed_schedules, cookie, codsis)


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

def set_schedules_for_today(all_schedules, cookie, codsis):
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

def main():
	if not os.path.isdir(APP_FOLDER_PATH):
			os.makedirs(APP_FOLDER_PATH)

	if (os.path.exists(SESSION_FILE_PATH)):
		session_file = open(SESSION_FILE_PATH, 'r')
		data = session_file.read().split('\n')
		codsis = data[0]
		cookie = {'jwt': data[1]}
		session_file.close()
	else :
		guiUILogin = UILogin()
		guiUILogin.mainloop()
		codsis = guiUILogin.logged_codsis
		cookie = guiUILogin.logged_cookie
	request_manager = DataRequests()
	response_data = request_manager.requestGet(sisCode=codsis, cookie=cookie)
	all_schedules = response_data['schedules']
	last_connection = datetime.strptime( response_data['last_connection'], RESPONSE_LAST_CONNECTION_FORMAT)
	
	send_catchup_reports(last_connection.replace(tzinfo=None), cookie, all_schedules, codsis)
	start_tray_icon()

	while True:
		set_schedules_for_today(all_schedules, cookie, codsis)
		tomorrow = datetime.now() + timedelta(days=1)
		difference = (datetime.combine(tomorrow, time.min) - datetime.now()).seconds + 60 #just in case addition
		thread_time.sleep(difference)

if __name__ == "__main__":
	main()
