from settings import *
# import MySQLdb
import mysql

'''
columns:
count
date
time
url
subdomain
domain
tld
rest
country
region
city
zip_code
lat
lon

'''




'''print 'connecting...'
db = MySQLdb.connect(host=settings['db_host'], user=settings['db_user'], passwd=settings['db_pw'], db=settings['db_table'])

print 'cursor...'
cursor = db.cursor()

print 'querying...'
cursor.execute('SELECT * FROM `connections`')

print 'closing connection...'
db.close()

print 'done'

'''