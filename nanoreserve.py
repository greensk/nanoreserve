#!/usr/bin/python
# * coding: utf8 *
# :TODO: archivation
# :TODO: exception handling
# :TODO: email output
# :TODO: ssh output
import simplejson
import sys
import time
import os
import subprocess
import shutil
import email
import smtplib

defaultConfig = {"input" : {}, "output" : [], "options" : {"tempDir" : "/tmp", "arch" : "gzip", "archSuffix" : "gz", "tempPrefix" : "nanoreserve"}}

if len(sys.argv) == 1:
	configFile = '/etc/nanoreserve.json'
else:
	configFile = sys.argv[1]

config = simplejson.loads(open(configFile).read())

config = dict(defaultConfig.items() + config.items())
	
tmp = config['options']['tempDir'] + '/' + config['options']['tempPrefix'] + '_' + str(int(time.time()))
os.mkdir(tmp)

files = []

for iId in config['input']:
	
	print 'input ' + iId + ':'
	item = config['input'][iId]
	
	if item['type'] == 'fs':
		outfile = '%s/%s.tar' % (tmp, iId)
		pdump  = subprocess.Popen(['tar', '-cOvvf', '-', item['path']], stdout=subprocess.PIPE)
		
	elif item['type'] == 'mysql':
		outfile = '%s/%s.sql' % (tmp, iId)
		args = ['mysqldump']
		if 'host' in item:
			args += ['-h', item['host']]
		if 'user' in item:
			args += ['-u', item['user']]
		if 'password' in item:
			args += ['--password=%s' % item['password']]
		if 'database' in item:
			args += [item['database']]
			
		pdump  = subprocess.Popen(args, stdout=subprocess.PIPE)
		
	else:
		print 'Error: unknown type %s' % item['type']
		continue
		
	outfile += '.' + config['options']['archSuffix']
	f = open(outfile, 'w')
	parch = subprocess.Popen(config['options']['arch'], stdin=pdump.stdout, stdout=f)
	pdump.stdout.close()
	parch.communicate()
	files.append(outfile)
	
for item in config['output']:
	
	if item['type'] == 'fs':
		print 'output ' + item['path'] + ':'
		for f in files:
			shutil.copy(f, item['path'])
	elif item['type'] == 'email':
		msg = email.MIMEMultipart.MIMEMultipart()
		msg['Subject'] = item['subject'] 
		msg['From'] = item['from']
		msg['To'] = ', '.join(item['to'])
		
		for f in files:
			part = email.MIMEBase.MIMEBase('application', "octet-stream")
			part.set_payload(open(f, "rb").read())
			email.Encoders.encode_base64(part)

			part.add_header('Content-Disposition', 'attachment; filename="%s"' % (os.path.basename(f)))
			msg.attach(part)
			
		server = smtplib.SMTP(item['smtp']['host'], item['smtp']['port'])
		if ('login' in item['smtp']):
			server.login(item['smtp']['login'], item['smtp']['password'])
		server.sendmail(item['from'], item['to'], msg.as_string())
		server.quit()

	else:
		print 'Error: unknown type %s' % item['type']

shutil.rmtree(tmp)
