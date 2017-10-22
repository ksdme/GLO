#!/usr/bin/python

import sys
import time
import argparse, json
from glo import GLO
from PySide.QtCore import *
from PySide.QtGui import *
from subprocess import Popen, PIPE
from PySide.QtDeclarative import QDeclarativeView

defaultKeys = GLO.defaultKeyStoreUrl(".glo/keys.json")
defaultPrefs = GLO.defaultKeyStoreUrl(".glo/prefs.json")

argParser = argparse.ArgumentParser()
argParser.add_argument("-k", "--keys", type=str, default=defaultKeys, help="Twitter API Keys")
argParser.add_argument("-p", "--prefs", type=str, default=defaultPrefs, help="Preference Keys")

parsed = argParser.parse_args()

# load the Glo Instance
glo = GLO(parsed.keys, parsed.prefs)
every = int(glo.getPref("every"))

while True:

	# sleep a moment
	time.sleep(every)

	# refresh prefs
	glo.reloadPrefs()

	# get connected flag 
	if not GLO.getIsConnected():
		continue

	# run UI for OP
	command = [
		"python",
		"gloUI.py", "-u", glo.getLoggedUser(),
		"-l", glo.getLastTweetTimeAsLabel(),
		"-i", str(glo.getPref("duration"))
	]

	# enable shell to use aliases in future
	result = Popen(" ".join(command), shell=True, stdout=PIPE)
	result.wait()

	# result as json
	resultJson = result.stdout.read().strip()
	resultJson = json.loads(resultJson)

	if resultJson["ok"]:
		try:
			result = glo.postTweet(resultJson["tweet"])
			print "[!] Send Tweet Status: {}".format(result)
		except: pass
	else:
		print "[!] Tweet Cancelled!"
