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

# :TODO: utility code

os.removedirs(tmp)
