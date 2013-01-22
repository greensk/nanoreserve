#!/usr/bin/python
# * coding: utf8 *
import simplejson
import sys
import time
import os
import subprocess
import shutil

defaultConfig = {"input" : {}, "output" : [], "options" : {"tempDir" : "/tmp", "arch" : "gzip", "tempPrefix" : "nanoreserve"}}

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
