import sys
import os
import re
import time
import json
import csv

# {domain: {CNAME: cname, IP: ip, PORT: port}}
# deal with value
def processing(**kwargs):
	global allvalue
	try:
		# {'domain':'domain','ip':'ip'}
		if kwargs.get('domain'):
			domain = kwargs.get('domain')
			# if domain exists, dict remains unchanged, otherwise create it
			allvalue.setdefault(domain,{})

			# determine whether there is specific key
			if 'cname' in kwargs.keys():
				# if cname exists, do nothing ,otherwise assign a empty list
				domain_value = allvalue[domain]
				domain_value.setdefault('cname',[])
				cname_value = kwargs['cname'].replace('CNAME ','')
				if cname_value.strip():
					if ',' in cname_value:
						cnames = cname_value.strip().split(',')
						for cname in cnames:
							# if new cname value in the list
							if cname:
								if cname in domain_value['cname']:
									pass
								else:
									domain_value['cname'].append(cname)
					else:
						domain_value['cname'].append(cname_value)

			if 'ip' in kwargs.keys():
				domain_value = allvalue[domain]
				domain_value.setdefault('ip',[])
				ip_value = kwargs['ip']
				# determine if ip in kwargs is a list
				if ip_value:
					if ',' in ip_value.strip():
						ips = ip_value.strip().split(',')
						for ip in ips:
							if ip:
								if ip in domain_value['ip']:
									pass
								else:
									domain_value['ip'].append(ip.strip())

					# ip in kwargs is a string
					else:
						domain_value['ip'].append(ip_value)

			if 'port' in kwargs.keys():
				domain_value = allvalue[domain]
				domain_value.setdefault('port',[])
				port_value = kwargs['port']
				if port_value.strip():
					if ',' in port_value:
						ports = port_value.strip().split(',')
						for port in ports:
							if port:
								if port in domain_value['port']:
									pass
								else:
									domain_value['port'].append(port)
					else:
						domain_value['port'].append(port_value)
		else:
			print(f'Error,no domain value')
	except Exception as e:
		print('Processing: ' + str(e))


# esd
def esd(path):
	global alltools
	if 'ESD' not in alltools:
		alltools.append('ESD')

	print(f'[ Notice ] ESD: processing file ** {path} **')
	try:
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
				processing(**value_dic)

	except Exception as e:
		print('esd: ' + str(e))

# subdomainbrute
def subdomainbrute(path):
	global alltools
	if 'subdomainbrute' not in alltools:
		alltools.append('subdomainbrute')

	print(f'[ Notice ] subdomainbrute: processing file ** {path} **')
	try:
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
				processing(**value_dic)
	except Exception as e:
		print('subdomainbrute: ' + str(e))

# aquatone
def aquatone(path):
	global alltools
	if 'aquatone' not in alltools:
		alltools.append('aquatone')

	print(f'[ Notice ] aquatone: processing file ** {path} **')
	try:
		with open(path,'r') as file:
			data = json.load(file)
			for domain in data.keys():
				ip = data[domain]
				# dict data
				value_dic = {'domain': domain.strip(), 'ip': ip.strip()}
				processing(**value_dic)

	except Exception as e:
		print('aquatone: ' + str(e))

# fierce
def fierce(path):
	global alltools
	if 'fierce' not in alltools:
		alltools.append('fierce')

	print(f'[ Notice ] fierce: processing file ** {path} **')
	try:
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
					processing(**value_dic)
				else:
					pass
	except Exception as e:
		print('fierce: ' + str(e))

def findomain(path):
	global alltools
	if 'findomain' not in alltools:
		alltools.append('findomain')

	print(f'[ Notice ] findomain: processing file ** {path} **')
	try:
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
				processing(**value_dic)
							
	except Exception as e:
		print('findomain: ' + str(e))

def chaos(path):
	global alltools
	if 'chaos' not in alltools:
		alltools.append('chaos')

	print(f'[ Notice ] chaos: processing file ** {path} **')
	try:
		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processing(**value_dic)
	except Exception as e:
		print('chaos: ' + str(e))

def assetfinder(path):
	global alltools
	if 'assetfinder' not in alltools:
		alltools.append('assetfinder')

	print(f'[ Notice ] assetfinder: processing file ** {path} **')
	try:
		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processing(**value_dic)
	except Exception as e:
		print('assetfinder: ' + str(e))

def ctfr(path):
	global alltools
	if 'ctfr' not in alltools:
		alltools.append('ctfr')

	print(f'[ Notice ] ctfr: processing file ** {path} **')
	try:
		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processing(**value_dic)
	except Exception as e:
		print('ctfr: ' + str(e))

def github_subdomains(path):
	global alltools
	if 'github_subdomains' not in alltools:
		alltools.append('github_subdomains')

	print(f'[ Notice ] github_subdomains: processing file ** {path} **')
	try:
		with open(path,'r') as file:
			for raw in file:
				domain = raw.strip().replace('*.','')
				# dict data
				value_dic = {'domain': domain.strip()}
				processing(**value_dic)
	except Exception as e:
		print('github_subdomains: ' + str(e))

def knock(path):
	global alltools
	if 'knock' not in alltools:
		alltools.append('knock')

	print(f'[ Notice ] knock: processing file ** {path} **')
	try:
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
				processing(**value_dic)

	except Exception as e:
		print('knock: ' + str(e))

def ksubdomain(path):
	global alltools
	if 'ksubdomain' not in alltools:
		alltools.append('ksubdomain')

	print(f'[ Notice ] ksubdomain: processing file ** {path} **')
	try:
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
				processing(**value_dic)

	except Exception as e:
		print('ksubdomain: ' + str(e))



def dnsmap(path):
	global alltools
	if 'dnsmap' not in alltools:
		alltools.append('dnsmap')

	print(f'[ Notice ] dnsmap: processing file ** {path} **')
	try:
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
						processing(**value_dic)
	except Exception as e:
		print('dnsmap: ' + str(e))

def tools(ROOT):
	try:
		for filename in os.listdir(ROOT):
			path = os.path.join(ROOT, filename)
			
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
	except Exception as e:
		print('Tools: ' + str(e))

def write_in(path):
	global allvalue

	try:
		with open(path,'w+', newline='') as file:
			file_write = csv.writer(file)
			file_write.writerow(['Domain', 'CNAME', 'IP', 'Ports'])
			# format data
			for domain in allvalue.keys():
				value_dic = allvalue.get(domain)
				cips = []
				for keys in value_dic.keys():
					cips.append(keys)
				all_value = ''.join(cips)
				if 'ip' in all_value:
					if value_dic.get('ip'):
						ip = value_dic.get('ip')
						ip = ','.join(set(ip))
					else:
						ip = ''
				else:
					ip = ''
				if 'cname' in all_value:
					if value_dic.get('cname'):
						cname = value_dic.get('cname')
						cname = ','.join(set(cname))
					else:
						cname = ''
				else:
					cname = ''
				if 'port' in all_value:
					if value_dic.get('port'):
						port = value_dic.get('port')
						port = ','.join(set(port))
					else:
						port = ''
				else:
					port = ''
				
				write_data = [domain, cname, ip, port]

				# write data
				file_write.writerow(write_data)
				# print(write_data)


	except Exception as e:
		print('write: ' + str(e))

if __name__ == '__main__':
	# {domain: {CNAME: cname, IP: ip, PORT: port}}

	logo = r"""
______                _ _  ______ _ _      
| ___ \              | | | |  ___(_) |     
| |_/ /___  ___ _   _| | |_| |_   _| | ___ 
|    // _ \/ __| | | | | __|  _| | | |/ _ \
| |\ \  __/\__ \ |_| | | |_| |   | | |  __/
\_| \_\___||___/\__,_|_|\__\_|   |_|_|\___|   A total of 12 
                                           
                                           
"""
                                
	print(logo)
	try:
		allvalue = {}
		alltools = []

		ROOT = "C:\\Users\\DC\\Desktop\\result\\"
		result = "C:\\Users\\DC\\Desktop\\"
		if os.path.exists(ROOT):
			print('Start subdomain result file processing...\n')
			
			tools(ROOT)
			write_in(result + 'result.csv')

			print(f'\n[ SUCCESS ] All files has been processed, a total of {len(alltools)} : \n\t{alltools} \n')
			print(f"[ OUTPUT ] Save csv output  to {result}result.csv): \n")
		else:
			print("[ Error ] Result file does not exists")
			sys.exit(1)
	except Exception as e:
		print('Main: ' + str(e))
	except KeyboardInterrupt:
		sys.stdout.write("\n\nWho stopped my program!\n")
	
