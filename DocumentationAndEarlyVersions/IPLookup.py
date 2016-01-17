
'''
IP LOOKUP
Jeff Thompson | 2015 | www.jeffreythompson.org

'''

import urllib2, json, os


offset = 		1
url = 			'http://freegeoip.net/'
num_read = 		0
max_to_read = 	10000


print 'IP LOOKUP'
if not os.path.isfile('AllServers_IP.csv'):
	print 'Creating file...'
	with open('AllServers_IP.csv', 'w') as o:
		o.write('count,date,time,server,ip,country,region,city,zip_code,lat,lon\n')


with open('AllServers.csv') as f:
	if offset > 0:
		print 'Jumping ahead by ' + str(offset) + ' lines...'
		for i in xrange(offset):
			f.next()

	print 'Getting IP info...'
	for i, line in enumerate(f):
		print '\n' + str(i+1) + ':',

		# reached the max, stop for now
		if num_read == max_to_read:
			print '\n' + 'Max reached! Current offset: ' + str(num_read)
			print '(you\'ll have to wait an hour for more...)'
			break

		# get data from original file
		line = line.strip()
		data = line.split(',')
		count = data[0]
		date = data[1]
		time = data[2]
		server = data[3]
		print server

		# get the IP data
		try:
			j = json.load(urllib2.urlopen(url + '/json/' + server))
			ip = 		str(j['ip'])
			country = 	str(j['country_name'])
			region = 	str(j['region_name'])
			city = 		str(j['city'])
			zip_code = 	str(j['zip_code'])
			lat = 		str(j['latitude'])
			lon = 		str(j['longitude']) 
			print '- found IP data!'
			
		# no data? probably a local URL
		except:
			ip = region = city = zip_code = lat = lon = ''
			print '- no IP data for that address :('

		# write to new file
		with open('AllServers_IP.csv', 'a') as o:
			o.write(count + ',' + date + ',' + time + ',' + server + ',' + ip + ',' + country + ',' + region + ',' + city + ',' + zip_code + ',' + lat + ',' + lon + '\n')

		# update count
		num_read += 1


# all done
print '\n\n'

