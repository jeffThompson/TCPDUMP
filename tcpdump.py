# -*- coding: utf-8 -*-

'''
▓▓▓▓▓░ ▓▓░  ▓▓▓░  ▓▓▓░  ▓░  ▓░ ▓▓░  ▓▓░ ▓▓▓░
  ▓░  ▓░ ▓░ ▓░ ▓░ ▓░ ▓░ ▓░  ▓░ ▓░▓ ▓░▓░ ▓░ ▓░
  ▓░  ▓░    ▓▓▓░  ▓░ ▓░ ▓░  ▓░ ▓░ ▓░ ▓░ ▓▓▓░
  ▓░  ▓░ ▓░ ▓░    ▓░ ▓░ ▓░  ▓░ ▓░    ▓░ ▓░
  ▓░   ▓▓░  ▓░    ▓▓▓░   ▓▓▓░  ▓░    ▓░ ▓░

Jeff Thompson | 2014-15 | www.jeffreythompson.org

An online performance, documenting every server my computer
connects to over a period of one month.

'''


# REQUIRED IMPORTS
from settings import ftp_settings
from functions import *
import os, socket, sys, pwd, glob, grp, time
from threading import Thread
from datetime import datetime
from subprocess import *


# SETUP VARIABLES
compare_stored_urls = 	True				# store unique (true) or all?
group_email_urls = 		True 				# combine 'perfora.net' urls?
col_width = 			10					# width of the "count" column
upload_interval = 		10 * 1000			# how often to re-upload index.php
log_filename = 			'AllServers.csv'

# tlds that aren't really tlds
not_really_tlds = 		[ 'imap', 'imaps', 'ftp' ]

# COLORS
ALL_OFF = 				'\033[0m'
BOLD = 					'\033[1m'
FG_CYAN = 				'\033[36m'
REVERSE = 				'\033[7m'

# PRINT CONTROL
CLEAR_LINE = 			'\x1b[1A'
CURSOR_UP = 			'\x1b[2K'

# ETC
count = 				0
prev_millis = 			millis()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# HI
os.system('cls' if os.name=='nt' else 'clear')
title = [ "______ ____    ____",
"/\\__  _/\\  _ `\\/\\  _ `\\",
"\\/_/\\ \\\\ \\ \\/\\_\\ \\ \\_\\ \\",
"   \\ \\ \\\\ \\ \\/_/\\ \\  __/",
"    \\ \\ \\\\ \\ \\_\\ \\ \\ \\/",
"     \\ \\_\\\\ \\____/\\ \\_\\",
"      \\/_/ \\/___/  \\/_/",
"____   __  __    _   _   ____",
"/\\  _ `\\/\\ \\/\\ \\  / \\_/ \\/\\  _ `\\",
"\\ \\ \\/\\ \\ \\ \\ \\ \\/\\      \\ \\ \\_\\ \\",
" \\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\__\\ \\ \\  __/",
"  \\ \\ \\_\\ \\ \\ \\_\\ \\ \\ \\_/\\ \\ \\ \\/",
"   \\ \\____/\\ \\_____\\ \\_\\\\ \\_\\ \\_\\",
"    \\/___/  \\/_____/\\/_/ \\/_/\\/_/" ]

for line in title:
	print FG_CYAN + BOLD + center_text(line) + ALL_OFF
print '\n' + FG_CYAN + center_text('A 24-Hour Performance Documenting Server Connections') + ALL_OFF
print '\n\n' + REVERSE + BOLD + center_text('SETUP') + ALL_OFF + '\n'


# LET US KNOW THE SETTINGS
print 'Combine email URLs:           ',
if group_email_urls:
	print FG_CYAN + BOLD + 'Yes' + ALL_OFF
else:
	print FG_CYAN + BOLD + 'No' + ALL_OFF

print 'Unique URLs only:             ',
if compare_stored_urls:
	print FG_CYAN + BOLD + 'Yes' + ALL_OFF
else:
	print FG_CYAN + BOLD + 'No' + ALL_OFF


# GET LOCAL DOMAIN
# ignore traffic from our own computer
print 'Ignoring local domain:',
local_domain = socket.gethostname()
local_domain = local_domain[:local_domain.rfind('.')]
local_domain = local_domain.lower()
print FG_CYAN + BOLD + '        ' + local_domain + ALL_OFF


# LOAD PREVIOUS URLS
# and prev count, start time, etc
print 'Gathering previous URLs...',
sys.stdout.flush()
previous_urls = set()
try:
	with open('AllServers.csv') as f:
		for i, line in enumerate(f):
			if i == 0:
				continue
			data = line.split(',')
			if i == 1:
				start_time = data[1] + ' at ' + data[2]
			previous_urls.add(data[3].strip())
		count = int(data[0])
except:
	with open('AllServers.csv', 'a') as f:
		f.write('count,date,time,url,subdomain,domain,tld,rest,ip,country,region,city,zip_code,lat,lon' + '\n')
	start_time = datetime.now().strftime('%B %d, %Y at %H:%M:%S')

print '\b\b\b\b:       ' + FG_CYAN + BOLD + 'Found ' + str(len(previous_urls)) + ' URLs' + ALL_OFF


# WHEN DID WE START?
# gathered from previous file or current time above
print 'Start time:                    ' + FG_CYAN + BOLD + start_time + ALL_OFF


# SET PERMISSIONS
# required to run tcpdump from Python
# or run manually first: sudo chown $USER:admin /dev/bp*
print 'Setting /dev/bp* permissions...',
sys.stdout.flush()
uid = pwd.getpwuid(os.getuid()).pw_name
uid = pwd.getpwnam(uid).pw_uid
gid = grp.getgrnam('admin').gr_gid
for f in glob.glob('/dev/bp*'):
	os.chown(f, uid, gid)
print '\b\b\b\b:  ' + FG_CYAN + BOLD + 'Set' + ALL_OFF


# RUN IT!
print '\n\n' + REVERSE + BOLD + center_text('GATHERING') + ALL_OFF + '\n'
print r_align('Count', col_width) + '   ' + 'Server'
try:
	while True:

		# RUN TCPDUMP
		# l = print output as single line
		# q = quiet
		# S = helps prevent "state accumulation" (ie memory leak)
		# p = promiscuous mode (should capture as much traffic as possible)
		p = Popen( [ 'sudo', 'tcpdump', '-lqSp' ], stdout=PIPE, stderr=STDOUT)
		
		# iterate results
		for row in iter(p.stdout.readline, 'b'):
			count += 1

			# parse URL from tcpdump
			url = parse_url(row, local_domain, group_email_urls, 
							compare_stored_urls, previous_urls)
			if url == None:
				continue
			print FG_CYAN + r_align(str(count), col_width) + '   ' + BOLD + url + ALL_OFF

			# split URL into parts
			url_parts = split_url(url, not_really_tlds)

			# get location for address
			location = get_location(url)

			# log to file
			log_data(count, url, url_parts, location)
			# update_html(count, url, url_parts)

			# enough time passed? upload
			if millis() > prev_millis + upload_interval:
				print '\n' + center_text('[ uploading... ]'),
				sys.stdout.flush()
				try:
					t = Thread(target=upload, args=(log_filename, ftp_settings))
					t.start()
					t.join()
					print CURSOR_UP + CLEAR_LINE + BOLD + center_text('[ uploading... DONE! ]') + ALL_OFF
				except:
					print CURSOR_UP + CLEAR_LINE + BOLD + center_text('[ uploading... ERROR, COULDN\'T UPLOAD! ]') + ALL_OFF
				prev_millis = millis()
				

except KeyboardInterrupt:
	print '\b\b   '			# a hack: no ^C on exit :)

	print '\n' + REVERSE + BOLD + center_text('CLOSING') + ALL_OFF + '\n'

	# final upload
	print 'Final upload:      ' + BOLD + FG_CYAN,
	sys.stdout.flush()
	try:
		t = Thread(target=upload, args=(log_filename, ftp_settings))
		t.start()
		t.join()
		print 'Done' + ALL_OFF
	except:
		print 'Error uploading' + ALL_OFF

	# close it
	print 'Disconnecting FTP:  ' + BOLD + FG_CYAN + 'Closed' + ALL_OFF
	print 'Recorded URLS:      ' + BOLD + FG_CYAN + str(len(previous_urls)) + ' total' + ALL_OFF
	print 'Start time:         ' + FG_CYAN + BOLD + start_time + ALL_OFF
	print 'End time:           ' + FG_CYAN + BOLD + datetime.now().strftime('%B %d, %Y at %H:%M:%S') + ALL_OFF
	print FG_CYAN + '\n' + '[ bye bye ]' + ALL_OFF + '\n'


# all done!
sys.exit(0)

