
'''
▓▓▓░ ▓▓▓░ ▓▓▓░  ▓▓▓░  ▓░  ▓░ ▓▓░  ▓▓░ ▓▓▓░
 ▓░  ▓░▓░ ▓░ ▓░ ▓░ ▓░ ▓░  ▓░ ▓░▓ ▓░▓░ ▓░ ▓░
 ▓░  ▓░   ▓▓▓░  ▓░ ▓░ ▓░  ▓░ ▓░ ▓░ ▓░ ▓▓▓░
 ▓░  ▓░▓░ ▓░    ▓░ ▓░ ▓░  ▓░ ▓░    ▓░ ▓░
 ▓░  ▓▓▓░ ▓░    ▓▓▓░   ▓▓▓░  ▓░    ▓░ ▓░

Jeff Thompson | 2014-15 | www.jeffreythompson.org

Post every server my computer connects to.


USES THE BUILT-IN tcpdump COMMAND
+ Details:
	- http://www.tcpdump.org/tcpdump_man.html
+ Must run first (or run in Terminal):
	- sudo chown $USER:admin /dev/bp*

NOTES && IDEAS
+ previous method
	- tshark -f "port 53" (via: http://wiki.wireshark.org/CaptureFilters)
+ list of common ports
	- http://www.webopedia.com/quick_ref/portnumbers.asp
+ capture only packets going out?
	- ie: from > to (where "from" doesn't have my username)
+ lookup IP address and resolve (location, details, etc)?

+ using -X gives the ASCII rep of the packet header - post to Twitter?
	(....5........E.
	.i[7@.3....;....
	..........g.....
	.C.I......,C....
	......0....L.y..
	.(=B.?.N...~....
	...G...N..Z.W.L.
	O.J+...

'''

# REQUIRED IMPORTS
from subprocess import *
from datetime import datetime
from settings import settings
from ftplib import FTP
import atexit, re, os, locale, socket, pwd, glob, grp, sys
from threading import Thread
from time import sleep


# VARIABLES
compare_stored_urls = 	True			# ignore previously stored urls (True), or store ALL OF THEM! (False)
group_email_urls = 		True 			# combine 'perfora.net' urls?
col_width = 			10				# width of the "count" column for connections
connection_count = 		0				# how many connections have we made so far


# COLORS
ALL_OFF = 				'\033[0m'
BOLD = 					'\033[1m'
FG_CYAN = 				'\033[36m'
REVERSE = 				'\033[7m'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# CENTER AND RIGHT ALIGN TEXT IN TERMINAL
def center_text(s):
	length = len(s)
	width = int(os.popen('stty size', 'r').read().split()[1])
	half = (width - length)/2
	remaining = width - half - length
	return (' ' * half) + s + (' ' * remaining)

def r_align(s, col_width):
	return (' ' * (col_width-len(s))) + s


# WRITE TO LOG FILE
def write_data(count, url):
	with open(output_filename, 'a') as output:
		date = datetime.now().strftime('%m-%d-%Y')			# get date in month-day-year
		time = datetime.now().strftime('%H-%M-%S.%f')		# get time in HH-MM-SS.000
		output.write(str(count) + ',' + date + ',' + time + ',' + url + '\n')


# UPDATE HTML FILE WITH ENTRY
def update_html(new_entry):
	with open('index.php') as index:			# load html as a list
		html = index.readlines()
	html.insert(2, new_entry)					# insert new line first
	with open('index.php', 'w') as index:		# save result back to file
		index.write(''.join(html))


# CONNECT TO FTP SERVER
def connect_ftp():
	global ftp, username, password, directory
	ftp.login(username, password)
	ftp.cwd(directory)


# UPLOAD TO SERVER
# via: http://effbot.org/librarybook/ftplib.htm
def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext.lower() in ('.txt', '.htm', '.html', '.css', '.js', '.php'):
        ftp.storlines('STOR ' + file, open(file))
    else:
        ftp.storbinary('STOR ' + file, open(file, 'rb'), 1024)


# READ NETWORK CONNECTIONS!
def list_connections():
	global connection_count, previous_urls, ftp

	# l = print output as single line
	# q = quiet
	# S = helps prevent "state accumulation" (ie memory leak)
	# p = "promiscuous" mode (should capture as much traffic as possible)
	p = Popen( [ 'sudo', 'tcpdump', '-lqSp' ], stdout=PIPE, stderr=STDOUT)
	for row in iter(p.stdout.readline, 'b'):
		connection_count += 1
		row = row.strip()

		# skip non-HTTP traffic
		if 'tcp' not in row:
			continue

		# ignore ourselves, get who we're talking to instead
		url = row.split()[2]	# (aka src)
		dst = row.split()[4]
		if local_domain in url.lower():
			continue
		'''if local_domain in dst:
			url = src
		else:
			url = dst'''

		# format url nicely
		url = re.sub(r'\.https?', '', url)
		url = re.sub(r':$', '', url)
		if group_email_urls:
			if 'perfora.net' in url:
				url = re.sub(r'[perfora\.net\.][0-9]+', '', url)

		# if ignoring previously gathered urls...
		if compare_stored_urls:
			if url in previous_urls:
				continue
			else:
				previous_urls.add(url)

		# format and upload it
		# (run upload as a thread so it completes before quitting)
		num = locale.format('%d', connection_count, grouping=True)
		print FG_CYAN + r_align(num, col_width) + '   ' + BOLD + url + ALL_OFF

		write_data(connection_count, url)
		
		update_html('			<tr class="entry"><td class="count darkCyan">' + str(connection_count) + '</td><td class="url"><a href="http://' + url + '" target="_blank">' + url + '</a></td></tr>' + '\n')
		try:
			t = Thread(target=upload, args=(ftp, 'index.php'))
			t.start()
			t.join()
		except:
			# FTP disconnected after a long period? reconnect
			print (' ' * col_width) + '   ' + '- FTP disconnected, reconnecting...'
			connect_ftp()
			t = Thread(target=upload, args=(ftp, 'index.php'))
			t.start()
			t.join()


	# done, close tcpdump
	p.terminate()


# DISCONNECT FROM SERVER ON EXIT
def exit_handler():
	global previous_urls
	print 'Disconnecting FTP...',
	ftp.quit()
	print '\b\b\b\b:  ' + BOLD + FG_CYAN + 'Closed' + ALL_OFF
	print 'Recorded URLS:      ' + BOLD + FG_CYAN + str(len(previous_urls)) + ' total' + ALL_OFF
	print 'Start time:         ' + FG_CYAN + BOLD + start_time + ALL_OFF
	print 'End time:           ' + FG_CYAN + BOLD + datetime.now().strftime('%B %d, %Y at %H:%M:%S') + ALL_OFF
	print FG_CYAN + '\n' + '[ bye bye ]' + ALL_OFF + '\n'


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# SOME BASIC SETUP
locale.setlocale(locale.LC_ALL, 'en_US')
height, width = os.popen('stty size', 'r').read().split()
width = int(width)
height = int(height)


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


# GET LOCAL DOMAIN
# to ignore errant incoming traffic
print 'Ignoring local domain:',
local_domain = socket.gethostname()
local_domain = local_domain[:local_domain.rfind('.')]
local_domain = local_domain.lower()
print FG_CYAN + BOLD + '        ' + local_domain + ALL_OFF


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


# CREATE LIST FOR PREVIOUS URLs
print 'Gathering previous URLs...',
sys.stdout.flush()

if compare_stored_urls:
	store_what = 'unique'
else:
	store_what = 'all'
output_filename = 'AllNetworkConnections_' + store_what + '.csv'

# if there's already a file, load into set
previous_urls = set()
try:
	with open(output_filename) as f:
		for line in f:
			data = line.split(',')
			previous_urls.add(data[3].strip())

# if file doesn't exist, create and write header
except:
	with open(output_filename, 'a') as f:
		f.write('connection_number,date,time,url' + '\n')

print '\b\b\b\b:       ' + FG_CYAN + BOLD + 'Found ' + str(len(previous_urls)) + ' URLs' + ALL_OFF


# CONNECT TO FTP SERVER
print 'Connecting to FTP server...',
sys.stdout.flush()
ftp_address = settings['ftp_address']
username = settings['username']
password = settings['password']
directory = settings['directory']
ftp = FTP(ftp_address)
connect_ftp()
atexit.register(exit_handler)
print '\b\b\b\b:      ' + FG_CYAN + BOLD + 'Connected' + ALL_OFF


# SET PERMISSIONS
# or run manually first: sudo chown $USER:admin /dev/bp*
print 'Setting /dev/bp* permissions...',
sys.stdout.flush()
uid = pwd.getpwuid(os.getuid()).pw_name
uid = pwd.getpwnam(uid).pw_uid
gid = grp.getgrnam('admin').gr_gid
for f in glob.glob('/dev/bp*'):
	os.chown(f, uid, gid)
print '\b\b\b\b:  ' + FG_CYAN + BOLD + 'Set' + ALL_OFF


# WHEN DID WE START?
start_time = datetime.now().strftime('%B %d, %Y at %H:%M:%S')
print 'Start time:                    ' + FG_CYAN + BOLD + start_time + ALL_OFF


# RUN IT
print '\n\n' + REVERSE + BOLD + center_text('GATHERING') + ALL_OFF + '\n'
print r_align('Count', col_width) + '   ' + 'Server'
try:
	while True:
		list_connections()
except KeyboardInterrupt:
	print '\b\b   '			# a hack: no ^C on exit :)
	print '\n' + REVERSE + BOLD + center_text('CLOSING') + ALL_OFF + '\n'
sys.exit(0)

