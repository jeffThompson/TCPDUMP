
import csv, operator

log_filename = '../AllServers.csv'

data = csv.reader(open(log_filename), delimiter=',')
headers = ','.join(next(data, None)) + '\n'

url_sorted = sorted(data, key=operator.itemgetter(3), reverse=False)
with open('AllServers_URL.csv', 'w') as f:
	f.write(headers)
	for i, line in enumerate(url_sorted):
		if i==0:
			header = line
			continue
		f.write(','.join(line) + '\n')

print '- sorting by count'
with open(log_filename) as f:
	s = f.readlines()
	s.reverse()
with open('AllServers_DESC.csv', 'w') as f:
	f.write(headers)
	f.writelines(s)