import sys
import os
import re
import json
import csv
from . import processdata

# esd
def esd(path):
	try:
		global alltools
		global allfiles
		# put the processed filename into allfiles
		allfiles.append(path)

		# put the executed function into alltools
		if 'ESD' not in alltools:
			alltools.append('ESD')

		with open(path,'r') as file:
			for raw in file:
				data = re.sub(r' +','--',raw.strip())
				data_list = data.split('--')
				domain = data_list[0]
				if len(data_list) > 2:
					ip = ','.join(data_list[1:])
				else:
					ip = data_list[1]
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
				processdata.process(**value_dic)

	except Exception as e:
		print(' [ Error ] Toolsdata -> esd: ' + str(e))

# subdomainbrute
def subdomainbrute(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'subdomainbrute' not in alltools:
			alltools.append('subdomainbrute')

		with open(path,'r') as file:
			for raw in file:
				data = re.sub(r' +','--',raw.strip())
				data_list = data.split('--')
				domain = data_list[0]
				if len(data_list) > 2:
					ip = ','.join(data_list[1:])
				else:
					ip = data_list[1]
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> subdomainbrute: ' + str(e))

# aquatone
def aquatone(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'aquatone' not in alltools:
			alltools.append('aquatone')

		with open(path,'r') as file:
			data = json.load(file)
			for domain in data.keys():
				ip = data[domain]
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
				processdata.process(**value_dic)

	except Exception as e:
		print(' [ Error ] Toolsdata -> aquatone: ' + str(e))

# fierce
def fierce(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'fierce' not in alltools:
			alltools.append('fierce')

		with open(path,'r') as file:
			for raw in file:
				if 'Found' in raw:
					data = raw.strip().replace('Found: ','').replace(')','').replace('(','').split(' ')
					domain = data[0]

					if len(data) > 2:
						ip = ','.join(data[1:])
					else:
						ip = data[1]
					# dict data
					value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
					processdata.process(**value_dic)
				else:
					pass
	except Exception as e:
		print(' [ Error ] Toolsdata -> fierce: ' + str(e))

def findomain(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'findomain' not in alltools:
			alltools.append('findomain')

		with open(path,'r') as file:
			for raw in file:
				data = raw.strip().replace(']','').split(',[')
				domain = data[0]
				if len(data) > 2:
					port = ','.join(data[1:])
				else:
					port = data[1]
				# dict data
				value_dic = {'domain': domain.strip(), 'port': port.strip()}
				processdata.process(**value_dic)
							
	except Exception as e:
		print(' [ Error ] Toolsdata -> findomain: ' + str(e))

def chaos(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'chaos' not in alltools:
			alltools.append('chaos')

		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> chaos: ' + str(e))

def assetfinder(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'assetfinder' not in alltools:
			alltools.append('assetfinder')

		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> assetfinder: ' + str(e))

def ctfr(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'ctfr' not in alltools:
			alltools.append('ctfr')

		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> ctfr: ' + str(e))

def github_subdomains(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'github_subdomains' not in alltools:
			alltools.append('github_subdomains')

		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> github_subdomains: ' + str(e))

def knock(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'knock' not in alltools:
			alltools.append('knock')

		with open(path,'r') as file:
			raw_all = json.load(file)
			for data in raw_all:
				domain = data.get('domain')
				ips = data.get('ip')
				if len(ips) >1:
					ip = ','.join(ips)
				else:
					ip = ips[0]
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
				processdata.process(**value_dic)

	except Exception as e:
		print(' [ Error ] Toolsdata -> knock: ' + str(e))

def dnsmap(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'dnsmap' not in alltools:
			alltools.append('dnsmap')

		with open(path,'r') as file:
			raw_all = file.read()
			raw = re.sub(r'\nIP(|v6) address #\d: ',' ',raw_all)
			raw = re.sub(r'^\n','',raw)
			raw_list = raw.split('\n')
			domain = raw_list[0]
			for data in raw_list:
				if data:
					if 'warning' not in data:
						data_list = data.split(' ')
						domain = data_list[0]
						if len(data_list) > 2:
							ip = ','.join(data_list[1:])
						else:
						 	ip = data_list[1]
						# dict data
						value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
						processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> dnsmap: ' + str(e))

def ksubdomain(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)

		if 'ksubdomain' not in alltools:
			alltools.append('ksubdomain')

		with open(path, 'r', encoding='utf-8') as file:
			file = csv.reader(file)

			for raw in file:
				if raw and len(raw) == 1:
					data = raw[0].strip().split('=>')
					domain = data[0].strip()
					ips = []
					cnames = []
					for others in data[1:]:
						other = others.strip()
						if 'CNAME' in other:
							cnames.append(other.replace('CNAME ',''))
						else:
							ips.append(other)

					if ips:
						if len(ips) > 1:
							ip = ','.join(ips)
						else:
							ip = ips[0]
					else:
						ip = ''
					if cnames:
						if len(cnames) > 1:
							cname = ','.join(cnames)
						else:
							cname = cnames[0]
					else:
						cname = ''
				else:
					pass
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip(), 'cname': cname.strip()}
				processdata.process(**value_dic)

	except Exception as e:
		print(' [ Error ] Toolsdata -> ksubdomain: ' + str(e))

def subfinder(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)
		if 'subfinder' not in alltools:
			alltools.append('subfinder')

		second = []
		with open(path,'r')as file:
			for d_all in file:
				d_list = d_all.strip().replace('.shisu.edu.cn','').split('.')
				second.append(d_list[-1])
			for sedomain in set(second):
				domain = sedomain + '.shisu.edu.cn'
				# dict data
				value_dic = {'domain': domain.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(' [ Error ] Toolsdata -> subfinder: ' + str(e))

def dnsub(path):
	try:
		global alltools
		global allfiles
		allfiles.append(path)
		if 'dnsub' not in alltools:
			alltools.append('dnsub')

		with open(path, 'r', encoding='utf-8') as file:
			data_list = csv.reader(file)
			for i in data_list:
				domain = i[0].strip()
				ip = i[1].strip()
				cname = i[2].strip()
				# dict data
				value_dic = {'domain': domain.strip('\ufeff'), 'ip': ip.strip(), 'cname': cname.strip()}
				processdata.process(**value_dic)
	except Exception as e:
		print(f"[ Error ] dnsub: " + str(e))

def tools(ROOT):
	try:
		for filename in os.listdir(ROOT):
			path = os.path.join(ROOT, filename)
			# if filename is file, not a dir
			if os.path.isfile(path):
				# judgement file extension
				name, extension = os.path.splitext(filename)

				if '.esd' in filename:
					esd(path)

				if 'assetfinder' in filename:
					assetfinder(path)

				if 'ctfr' in filename:
					ctfr(path)

				if 'chaos' in filename:
					chaos(path)

				if 'dnsmap' in filename:
					dnsmap(path)

				if 'fierce' in filename:
					fierce(path)

				if 'findomain' in filename:
					findomain(path)

				if 'github_subdomains' in filename:
					github_subdomains(path)

				if 'hosts' in filename:
					aquatone(path)

				if 'subdomainbrute' in filename:
					subdomainbrute(path)

				if re.search(r'\d{4}_(\d{2}_)*\d{2}\.json',filename):
					knock(path)

				if 'ksubdomain' in filename and extension == '.csv':
					ksubdomain(path)

				if 'subfinder' in filename:
					subfinder(path)
				if 'dnsub' in filename:
					dnsub(path)

	except Exception as e:
		print(' [ Error ] Toolsdata -> Tools: ' + str(e))

def main(r_path):
	# {domain: {CNAME: cname, IP: ip, PORT: port}}
	# global variables
	global alltools
	global allfiles  

	try:
		alltools = []
		allfiles = []

		# perform tools function 
		tools(r_path)

		return alltools, allfiles
	except Exception as e:
		print(' [ Error ] Toolsdata ->  Main: ' + str(e))
	

