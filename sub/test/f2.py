import dict1

def main():
	for i in range(0,10):
		domain = 'domain'
		ip = i
		dic = {'domain': domain, 'cname': str(ip)}
		allvalue = dict1.processing(**dic)


