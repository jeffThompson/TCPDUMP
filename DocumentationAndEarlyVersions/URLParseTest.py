
'''

Via: http://stackoverflow.com/a/6427654/1167783
'''

import re

url = '197.21.1.testing.aws-1.amazon.edu.microsoft-ds'
# url = 'perfora.net.ftp'

pattern = '((https?|ftp)\:\/\/)?'										# scheme
pattern += '([a-z0-9+!*(),;?&=\$_.-]+(\:[a-z0-9+!*(),;?&=\$_.-]+)?@)?' 	# user and pass
pattern += '([a-z0-9-.]*)\.([a-z]{2,4})' 								# host or IP
pattern += '(\:[0-9]{2,5})?' 											# port
pattern += '(\/([a-z0-9+\$_-]\.?)+)*\/?' 								# path
pattern += '(\?[a-z+&\$_.-][a-z0-9;:@&%=+\/\$_.-]*)?' 					# GET query
pattern += '(#[a-z_.-][a-z0-9+\$_.-]*)?' 								# anchor
prog = re.compile(pattern)

m = prog.match(url)
if m:
	path = m.groups()[4]
	domain = path[path.rfind('.')+1:]
	tdl = m.groups()[5]
	subdomain = path[:path.find('.' + domain)]
	rest = url[url.find(domain + '.' + subdomain):]
	print '<span class="subdomain">' + subdomain + '</span><span class="domain">' + domain + '.' + tdl + '</span>' + '<span class="subdomain">' + rest + '</span>'
else:
	print '<span class="domain">' + url + '</span>'



