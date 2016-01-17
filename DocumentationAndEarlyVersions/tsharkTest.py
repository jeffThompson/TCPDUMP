
# from subprocess import *

p = Popen( [ 'sudo', 'tshark', '-f "port 53"' ], stdout=PIPE, stderr=STDOUT)
for row in iter(p.stdout.readline, 'b'):
	print row.strip()

# import pyshark

# capture = pyshark.LiveCapture(bpf_filter="port 53")
# capture.sniff(timeout=50)

# for packet in capture.sniff_continuously(packet_count=1):
# 	print packet