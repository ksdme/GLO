"""
	@author ksdme
"""
import os
from subprocess import call
from argparse import ArgumentParser

argParser = ArgumentParser()

# stop/restart current thread
subparsers = argParser.add_subparsers(dest="mode")

# Stop GLO Subparser
stopSub = subparsers.add_parser("stop", help='Stop GLO')

# the deed has been done
parsed = argParser.parse_args()

#----------- Utility Funcs -----------
def getPID(loc=None):
	if loc is None:
		loc = os.path.join(os.path.expanduser("~"), ".glo/.pid")

	try:
		with open(loc, "r") as locR:
			return int(locR.read())
	except:
		return None

# begin control flow stuff here
if parsed.mode == "stop":
	"""
		remembr the current method wont
		work if glo was started with root previls
	"""

	pid = getPID()
	if pid is not None:
		call(["kill", "-9", str(pid)])
		print "Killed process with", pid
	else:
		print "~/.glo/.pid missing"
