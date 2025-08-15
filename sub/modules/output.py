import csv
from . import config_var

def write_in(r_pathname,):
	try:
		allvalue = config_var.allvalue
		with open(r_pathname,'w+', newline='') as file:
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
		print(' [ Error ] output ->  write_in: ' + str(e))
