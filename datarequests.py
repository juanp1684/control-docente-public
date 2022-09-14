import json
from urllib import request, response
import requests

class DataRequests:
	
	def __init__(self):
		self.URL_API_REST = "https://control-docente.herokuapp.com/schedules"

	def requestGet(self, sisCode):
		response = requests.get(self.URL_API_REST + "?codsis=" + sisCode)
		print(response.json())

	def requestsPost(self, report):
		request = requests.post(self.URL_API_REST + "/report/", data=report)
		response = json.loads(request.content)
		print(response['message'])

	def createReport(self, result):
		dataResult = result.split(';')
		jsonData = '{"codsis": "' + dataResult[0] + '", "schedule_id": ' + dataResult[1] + ', "attempts": ' + dataResult[2] + ', "report_type": "' + dataResult[3] + '"}'
		return jsonData

dataRequests = DataRequests()
dataRequests.requestGet("201800124")
#dataRequests.requestGet("2222")
#data = "1111;5;3;fallido"
#dataRequests.requestsPost(dataRequests.createReport(data))