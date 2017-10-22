"""
	@author ksdme
	responsible for setting making the
	tweet, getting the last tweeted at
	string and giving out the internet
	status
"""
import json, requests
import os, time, twitter

class PreferenceMissing(Exception):
	def __init__(self, msg):
		super(PreferenceMissing, self).__init__(msg)

class GLO(object):

	@staticmethod
	def getIsConnected(max_tries=3, gap=2):
		endpoint = "https://api.ipify.org/?format=json"
		
		for _ in xrange(max_tries):
			try:
				requests.get(endpoint)
				return True
			except Exception as E:
				time.sleep(gap)
				continue

		return False

	@staticmethod
	def defaultKeyStoreUrl(append=""):
		return os.path.join(os.path.expanduser("~"), append)

	@staticmethod
	def loadStore(url):
		return open(url, "r").read()

	@staticmethod
	def defaultKeyStore():
		"""
			Currently works only for
			linux based systems
		"""
		return GLO.defaultKeyStoreUrl(".glo/keys.json")

	@staticmethod
	def defaultPrefsStore():
		""" again, linups only """
		return GLO.defaultKeyStoreUrl(".glo/prefs.json")

	@staticmethod
	def formatTimeInterval(interval):
		""" interval in seconds """
		interval = float(interval)

		# supports only a major label
		labels = [
			("s", 60), ("m", 60), ("h", 24),
			("d", 20), ("w", 7), (" months", 12),
			("y", 9999)
		]

		for label, mx in labels:
			if 0 < interval < mx:
				return "{}{}".format(
					int(interval), label)
			else:
				interval /= mx

	def __init__(self, store=None, prefs=None):
		if store is None:
			store = GLO.defaultKeyStore()

		if prefs is None:
			prefs = GLO.defaultPrefsStore()

		keys = json.loads(GLO.loadStore(store))
		prefVals = json.loads(GLO.loadStore(prefs))

		self._api = twitter.Api(**keys)
		self._prefs_addr = prefs
		self._prefs = prefVals
	
	def postTweet(self, text):
		if 0 < len(text) <= 140:
			self._api.PostUpdate(text)
			return True
		else:
			return False

	def getLastTweetTime(self):
		tweet = self._api.GetUserTimeline(count=1)[0]
		return int(tweet.created_at_in_seconds)

	def getLastTweetTimeAsLabel(self):
		return GLO.formatTimeInterval(time.time()-self.getLastTweetTime())

	def getPref(self, key):
		try:
			return self._prefs[key]
		except:
			raise PreferenceMissing("{} Missing!".format(key))

	def setPref(self, key, value):
		self._prefs[key] = value

	def reloadPrefs(self):
		self._prefs = json.loads(open(self._prefs_addr, "r").read())

	def getLoggedUser(self):
		tweet = self._api.GetUserTimeline(count=1)[0]
		return tweet.user.screen_name
