
import tldextract

def split_url(url, not_really_tlds):

	# set "rest" to blank, will be set below if exists
	rest = ''

	# check for non-TLDs (like ftp)
	# set "rest" to that value
	for non in not_really_tlds:
		if non in url:
			print '- found non tld!'
			url = url.replace(non, '')
			print '- setting <rest> to "' + non + '"'
			rest = non

	# split url
	u = tldextract.extract(url)
	print u
	# if u.suffix != '':
		# rest = url.split(u.domain + '.' + u.suffix, 1)[1]
	url_parts = (u.subdomain, u.domain, u.suffix, rest)

	return url_parts

not_really_tlds = [ 'ftp' ]

url = '104.25.234.23'
url = 'google-ggc.145.23.verizon.net'
# url = 'test.amazon.com'
url = 'testing.145.perfora.net.ftp'

parts = split_url(url, not_really_tlds)
print parts

