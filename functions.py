# -*- coding: utf-8 -*-

import os, re, time, tldextract, urllib2, json, socket, csv, operator
from ftplib import FTP
from datetime import datetime
from settings import ftp_settings

attempt_to_resolve_hostname_from_ip = True 		# try to get hostname from IP address?


# GET CURRENT TIME IN MILLISECONDS
def millis():
	return int(round(time.time() * 1000))


# CENTER AND RIGHT ALIGN TEXT IN TERMINAL
def center_text(s):
	length = len(s)
	width = int(os.popen('stty size', 'r').read().split()[1])
	half = (width - length)/2
	remaining = width - half - length
	return (' ' * half) + s + (' ' * remaining)

def r_align(s, col_width):
	return (' ' * (col_width-len(s))) + s


# SORT FILES FOR UPLOAD
def sort_files(log_filename):
	data = csv.reader(open(log_filename), delimiter=',')
	headers = ','.join(next(data, None)) + '\n'

	# sort by URL
	url_sorted = sorted(data, key=operator.itemgetter(3), reverse=False)
	with open('AllServers_URL.csv', 'w') as f:
		f.write(headers)
		for i, line in enumerate(url_sorted):
			if i==0:
				header = line
				continue
			f.write(','.join(line) + '\n')

	# reverse file to sort by count (descending)
	with open(log_filename) as f:
		s = f.readlines()
		s.reverse()
	with open('AllServers_DESC.csv', 'w') as f:
		f.write(headers)
		f.writelines(s)


# UPLOAD FILE TO SERVER
# connects each time to avoid timeout and other
# issues for long FTP connections
def upload():
	ftp_address = ftp_settings['ftp_address']
	username = ftp_settings['username']
	password = ftp_settings['password']
	directory = ftp_settings['directory']

	ftp = FTP(ftp_address)
	ftp.login(username, password)
	ftp.cwd(directory)

	files_to_upload = [ 'AllServers_ASC.csv', 'AllServers_DESC.csv', 'AllServers_URL.csv' ]
	for f in files_to_upload:
		ext = os.path.splitext(f)[1]
		if ext.lower() in ('.txt', '.htm', '.html', '.css', '.js', '.php', '.csv'):
			ftp.storlines('STOR ' + f, open(f))
		else:
			ftp.storbinary('STOR ' + f, open(f, 'rb'), 1024)
	ftp.quit()


# LOG DATA TO CSV FILE
# saves count, date, time, url
def log_data(count, url, parts, location):
	with open('AllServers.csv', 'a') as output:
		date = datetime.now().strftime('%m-%d-%Y')
		time = datetime.now().strftime('%H-%M-%S.%f')
		p = ','.join(parts)
		l = ','.join(location)
		output.write(str(count) + ',' + date + ',' + time + ',' + url + ',' + p + ',' + l + '\n')


# GET LOCATION FROM URL
def get_location(url):
	try:
		j = json.load(urllib2.urlopen('http://freegeoip.net/json/' + url))
		ip = 		str(j['ip'])
		country = 	str(j['country_name'])
		region = 	str(j['region_name'])
		city = 		str(j['city'])
		zip_code = 	str(j['zip_code'])
		lat = 		str(j['latitude'])
		lon = 		str(j['longitude'])
		location = (ip, country, region, city, zip_code, lat, lon)
	except:
		location = ('', '', '', '', '', '', '')
	return location


# IS THIS AN IP ADDRESS?
# checks url to see if it is an IP address
# returns True/False, (ip/address, extra bits)
def is_ip_address(url):

	# standard IP address?
	try:
		socket.inet_aton(url)

		# attempt to resolve IP to hostname
		if attempt_to_resolve_hostname_from_ip:
			try:
				host = socket.gethostbyaddr(url)
				return False, (host[0])
			except:
				pass

		return True, (url, '')
	except socket.error:
		pass

	# IP address with extra bits on it?
	ip_with_extras = re.match('(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\.(.*?)$', url)
	if ip_with_extras is not None:
		return True, (ip_with_extras.group(1), ip_with_extras.group(2))
	
	# not an IP address
	else:
		return False, (url, '')


# SPLIT URL
# returns tuple with url split into components
# (subdomain, domain, tld, rest)
def split_url(url, not_really_tlds):

	# few edge cases, hard-coded :(
	if url == 'nexus.stevens.edu.s.imap':
		return ('nexus', 'stevens', 'edu', 's.imap')
	elif url == 'perfora.net.s.imap':
		return ('', 'perfora', 'net', 's.imap')

	# set "rest" to blank, will be set below if exists
	rest = ''

	# check for non-TLDs (like ftp)
	# set "rest" to that value
	for non in not_really_tlds:
		if non in url:
			url = url.replace(non, '')
			if url.startswith('.'):
				url = url[1:]
			rest = non

	# my mobile devices?
	if 'jeffthonsiphone' in url:
		matches = re.match(r'jeffthonsiphone\.([a-z].*?)\.(.*?)$', url)
		return ('', 'jeffthompsonsiphone', matches.group(1), matches.group(2))
	if 'jeffs-ipad' in url:
		matches = re.match(r'jeffs-ipad\.([a-z].*?)\.(.*?)$', url)
		return ('', 'jeffs-ipad', matches.group(1), matches.group(2))

	# is this an IP address?
	# (ignore if ulr includes some basic TLDs)
	real_tlds = [ 'com', 'net', 'org' ]
	if any(('.' + ext) in url for ext in real_tlds) == False:
		ip_addr, parts = is_ip_address(url)
		if ip_addr:
			return('', parts[0], '', parts[1])

	# ok? split url
	u = tldextract.extract(url)
	return (u.subdomain, u.domain, u.suffix, rest)


# PARSE URL FROM TCPDUMP
# takes raw response from tcpdump and returns a url
# if not valid, returns None
def parse_url(row, local_domain, group_email_urls, compare_stored_urls, previous_urls):
	row = row.strip()
	url = row.split()[2]

	# skip non-HTTP traffic
	if 'tcp' not in row:
		return None

	# ignore ourselves
	if local_domain in url.lower():
		return None

	# simplify email URLs, if specified
	# (also ignore the insane # of Stevens sub-IPs... 🙄)
	if group_email_urls and 'perfora.net' in url:
		url = re.sub(r'[perfora\.net\.][0-9]+', '', url)
	if group_email_urls and '155.246.200.20' in url:
		return None

	# ignore 'link' and 'output' (always the first 2 URLs...)
	if url == 'link' or url == 'output':
		return None

	# format nicely
	url = re.sub(r'\.https?', '', url)
	url = re.sub(r':$', '', url)

	# have we already seen this URL?
	if compare_stored_urls:
		if url in previous_urls:
			return None
		else:
			previous_urls.add(url)

	# done
	return url

