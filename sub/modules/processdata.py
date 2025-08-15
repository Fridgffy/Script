from . import allvalue_dict

# allvalue: {domain: {'cname': [cname], 'ip': [ip], 'port': [port]},}
# deal with value
def process(**kwargs):
	try:
		# global allvalue
		allvalue = allvalue_dict.allvalue
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
			print(f' [ Error ] process -> kwargs no domain value')
	except Exception as e:
		print(' [ Error ] Processing -> process: ' + str(e))