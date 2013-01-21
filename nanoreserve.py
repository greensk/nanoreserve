#!/usr/bin/python
# * coding: utf8 *
import simplejson
import sys
import time
import os

defaultConfig = {"input" : {}, "output" : "", "options" : {"tempDir" : "/tmp", "arch" : "gzip", "tempPrefix" : "nanoreserve"}}

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
		# :TODO: fs dump command
		pass
	else:
		print 'Error: unknown type %s' % item['type']
	
for oId in config['output']:
	
	print 'output ' + oId + ':'
	item = config['output'][oId]
	
	if item['type'] == 'fs':
		# :TODO: fs copy command
		pass
	else:
		print 'Error: unknown type %s' % item['type']

os.removedirs(tmp)
