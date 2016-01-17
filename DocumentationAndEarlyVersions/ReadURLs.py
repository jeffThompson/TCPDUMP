
'''
READ URLs
Jeff Thompson | 2015 | www.jeffreythompson.org

Asyncronously reads aloud the URLs from TCPDUMP.

'''

import time, subprocess


# tracks file in real-time and reads
# when new URLs are published
def follow(f):
	f.seek(0,2)
	while True:
		line = f.readline()
		if not line:
			time.sleep(0.1)
			continue
		line = line.strip().split(',')
		yield line[3]


# do it
url_file = open('AllNetworkConnections_unique.csv', 'r')
url_file = follow(url_file)
for url in url_file:
	print url
	p = subprocess.check_call(['say', url])

