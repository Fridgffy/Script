import sys
import os
import re
import requests
import urllib
import time
import yaml
import json
import csv
import datetime
import argparse
import subprocess

class Incidents():
	def __init__(self, cookie, pagesize, old_name, newjsonfile, oldjsonfile):
		self.cookie = cookie
		self.pagesize = pagesize
		self.old_name = old_name
		self.oldjsonfile = oldjsonfile
		self.newjsonfile = newjsonfile

	# Get incident list
	def GetIncidentList(self):
		url = 'http://10.16.1.10:18080/docp/gateway/event/v1/artemis/incident/list?__timestap=1761121543135&lang=zh_CN&__timestap=1761121543154'
		data = {"currentPage":1,"pageSize":self.pagesize,"type":"ALL","processStatusList":["PENDING"],"orderCreateTime":2}
		HEADERS = {
		'Host':'10.16.1.10:18080',
		'Content-Length':'96',
		'accountId':'110',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
		'withCredentials':'true',
		'userId':'3',
		'Content-Type':'application/json',
		'Accept':'*/*',
		'Origin':'http://10.16.1.10:18080',
		'Referer':'http://10.16.1.10:18080/',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
		'Cookie': self.cookie,
		'Connection':'keep-alive'
		}
		try:
			response = requests.post(url, json=data, headers=HEADERS)
			if response.status_code == 200:
				data = response.json()
				incidentslist = [item.get("incidentId") for item in data.get("data", {}).get("list", [])]
				# incidents = [item.get("createdTime") for item in data.get("data", {}).get("list", [])]
				return incidentslist
			else:
				print(f"Error! request status code: {response.status_code}")
		except Exception as e:
			print(str(e))


	# Get single incident
	def GetSingleIncident(self, incidentid):
		url = f'http://10.16.1.10:18080/docp/gateway/event/v1/artemis/incident/get/{incidentid}?__timestap=1761122715468&lang=zh_CN&__timestap=1761122715482'
		headers = {
		'Host':'10.16.1.10:18080',
		'accountId':'110',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
		'withCredentials':'true',
		'userId':'3',
		'Accept':'*/*',
		'Referer':'http://10.16.1.10:18080/',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
		'Cookie': self.cookie,
		'Connection':'keep-alive'
		}
		try:
			res = requests.get(url=url, headers=headers)
			result = json.loads(res.text).get('data')
			tagname = result.get('incidentName')
			for tag in tagname.get('tags'):
				name = tag.get('tagName')
				if name == 'targetname':
					incidentname = tag.get('tagValue')
				if name == 'device_ip':
					incidentip = tag.get('tagValue')
				if name == 'device_group':
					incidentgroup = tag.get('tagValue')
			if result.get("level") == 'MODERATE':
				level_zh = '次要的'
			elif result.get("level")== 'MINOR':
				level_zh = '提示'
			else:
				level_zh = result.get("level")
			# determine wether level equal OK
			if level_zh != 'OK':
				result_json = {
				"level": level_zh,
				# "level": result.get("level"),
				"highestLevel": result.get("highestLevel"),
				"incidentname": incidentname,
				"incidentip": incidentip,
				"incidentgroup": incidentgroup,
				# check items
				"checks": result.get("checks"),
				# incident description
				"description": result.get("description"),
				"createdTime": str(datetime.datetime.fromtimestamp(int(result.get("createdTime"))/1000).strftime("%Y-%m-%d %H:%M:%S")),
				"updatedTime": str(datetime.datetime.fromtimestamp(int(result.get("updatedTime"))/1000).strftime("%Y-%m-%d %H:%M:%S")),
				# "alertCount": result.get("alertCount"),
				# "resultNameText": result.get("resultNameText")
				}
			else:
				result_json = ''
			return result_json
		except Exception as e:
			print(str(e))

	# Deal with the result json data
	def DealwithData(self):
		try:
			jsonlist_old = []
			jsonlist = []
			jsondic = {'old': '', 'new': ''}
			
			# Get incidents list, incoude 15 incident
			incidentslist = self.GetIncidentList()
				
			# Interate through the incident list
			for incidentid in incidentslist:
				# Get single incident
				result_json = self.GetSingleIncident(incidentid)
				time.sleep(0.2)
				# determine whether result json is empty
				if result_json:
					# Determine whether the incident name is in the old name list
					if result_json.get('incidentname') in self.old_name:
						jsonlist_old.append(result_json)
					else:
						jsonlist.append(result_json)

			jsondic['old'] = jsonlist_old
			jsondic['new'] = jsonlist

			# Write the list of new and old incidents  to a json file
			with open(self.newjsonfile, 'w', encoding='utf-8') as file_new:
				file_new.write(str(jsondic.get('new')).replace('\'','\"'))
			with open(self.oldjsonfile, 'w', encoding='utf-8') as file_old:
				file_old.write(str(jsondic.get('old')).replace('\'','\"'))
		except Exception as e:
			print(str(e))

if __name__ == '__main__':
	logo = r"""
 _____           _     _            _       _     _     _   
|_   _|         (_)   | |          | |     | |   (_)   | |  
  | | _ __   ___ _  __| | ___ _ __ | |_ ___| |    _ ___| |_ 
  | || '_ \ / __| |/ _` |/ _ \ '_ \| __/ __| |   | / __| __|
 _| || | | | (__| | (_| |  __/ | | | |_\__ \ |___| \__ \ |_ 
 \___/_| |_|\___|_|\__,_|\___|_| |_|\__|___|_____/_|___/\__|

"""
	print(logo)
	try:
		CONFIG = './config.yml'
		INTERVAL = 20
		COUNT = 0

		parser = argparse.ArgumentParser(description="Choose automatic or manual refresh")
		parser.add_argument('-a', '--automatic', action='store_true', help='Automatic refresh')
		parser.add_argument('-m', '--manually', action='store_true', help='Manually refresh')
		args = parser.parse_args()

		with open(CONFIG, 'r', encoding='utf-8') as file:
			# extract cookie
			config_dict = yaml.safe_load(file)

			cookie = config_dict['cookie']
			newjsonfile = config_dict['newjsonfile']
			oldjsonfile = config_dict['oldjsonfile']
			old_name = config_dict['old_name']
			pagesize = config_dict['pagesize']

		incident = Incidents(cookie, pagesize, old_name, newjsonfile, oldjsonfile)

		# manually refresh
		if args.manually:
			sys.stdout.write('[ Notice ] Manual refresh, press Enter to execute\n')
			while True:
				input()
				incident.DealwithData()
				p = subprocess.Popen('START chrome http://127.0.0.1:8000/portal.html', text=True, shell=True, stdout=None, stderr=subprocess.PIPE)
				# p = subprocess.Popen('START chrome http://127.0.0.1:8000/desktop/GetIncident/portal.html', text=True, shell=True, stdout=None, stderr=subprocess.PIPE)
				sys.stdout.write(f'[ {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ] Program execution successfully!')
		# automatic refresh
		else:
			if args.automatic:
				sys.stdout.write('[ Notice ] Automatic refresh, once every 10 minutes\n\n')
			else:
				sys.stdout.write('[ Notice ] No parameters are specified, the default is to refresh automatically\n\n')

			while True:
				incident.DealwithData()
				COUNT += 1
				sys.stdout.write(f'\r[ {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ] The program was successfully execution {COUNT} times')
				time.sleep(INTERVAL)
	except Exception as e:
		print(str(e))
	except KeyboardInterrupt:
		print("谁把我程序停了!")
