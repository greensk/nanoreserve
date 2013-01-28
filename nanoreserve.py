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
		subprocess.call(['tar', '-czvvf', outfile, item['path']])
		files.append(outfile)
	elif item['type'] == 'mysql':
		outfile = '%s/%s.sql.%s' % (tmp, iId, config['options']['archSuffix'])
		args = ['mysqldump']
		if 'host' in item:
			args += ['-h', item['host']]
		if 'user' in item:
			args += ['-u', item['user']]
		if 'password' in item:
			args += ['--password=%s' % item['password']]
		if 'database' in item:
			args += [item['database']]
			
		f = open(outfile, 'w')
		pdump  = subprocess.Popen(args, stdout=subprocess.PIPE)
		parch = subprocess.Popen(config['options']['arch'], stdin=pdump.stdout, stdout=f)
		pdump.stdout.close()
		parch.communicate()
		
		files.append(outfile)
	else:
		print 'Error: unknown type %s' % item['type']
	
for item in config['output']:
	
	if item['type'] == 'fs':
		print 'output ' + item['path'] + ':'
		for f in files:
			shutil.copy(f, item['path'])
	else:
		print 'Error: unknown type %s' % item['type']

shutil.rmtree(tmp)
