'''
IP ADDRESS TEST

'''

import socket, re

def is_ip_address(url):
	''' checks url to see if it is an IP urless; returns True/False
	and (ip/address, extra bits)'''

	# standard IP address?
	try:
		socket.inet_aton(url)
		return True, (url, None)
	except socket.error:
		pass

	# IP address with extra bits on it?
	ip_with_extras = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.(.*?)$', url)
	if ip_with_extras is not None:
		return True, (ip_with_extras.group(1), ip_with_extras.group(2))
	
	# not an IP address :(
	else:
		return False, (url, None)

ip = '63.88.100.137'
ip = '17.172.232.12.5223'
ip = '152.14.117.63.piscataway.google-ggc.verizon.com'
ip = 'google.com.testing'

is_ip, address = is_ip_address(ip)
print is_ip
print address

url = 'jeffthonsiphone.home.afs3-fileserver'
matches = re.match(r'jeffthonsiphone\.([a-z].*?)\.(.*?)$', url)
print 'jeffthompsonsiphone'
print matches.group(1)
print matches.group(2)






