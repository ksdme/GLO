import sys
import argparse
from json import dumps
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView

# Context Injectable Properties
class InitialEnvironment(QObject):

	def __init__(self, user, last, interval):
		assert isinstance(interval, int)
		QObject.__init__(self)

		self._user = user
		self._last = last
		self._interval = interval

	def getUser(self): return self._user
	def getLast(self): return self._last
	def getInterval(self): return self._interval

	@Signal
	def dumbSignal(self):
		pass

	user = Property(unicode, getUser, notify=dumbSignal)
	last = Property(unicode, getLast, notify=dumbSignal)
	duration = Property(int, getInterval, notify=dumbSignal)

# make the default app window
qApp = QApplication(sys.argv)

# get all the args required
argParser = argparse.ArgumentParser()

# get last time and the username of the guy
argParser.add_argument("-u", "--user", help="Username of the guy", required=True)
argParser.add_argument("-l", "--last", help="Last Tweet time ago", required=True)
argParser.add_argument("-i", "--duration", help="Interval of Window (In Seconds)", type=int)

# parse the remaining args
parsed = argParser.parse_args()

# Signal Slots
@Slot()
def safelyQuitPlease():
	print dumps({
		"ok": False
	})

	# Close the App
	QCoreApplication.quit()

@Slot()
def submitedTweet(tweet):
	print dumps({
		"ok": True,
		"tweet": str(tweet)
	})	

	# Ideally Show a Tweeted msg
	# and then close the Messga
	QCoreApplication.quit()

#---------------------------
qView = QDeclarativeView()
qUrl = QUrl('./QML/main.qml')

# add the context first
qContext = qView.rootContext()
env = InitialEnvironment(parsed.user, "{} ago".format(parsed.last), parsed.duration)
qContext.setContextProperty("environment", env)

# and then set source
qView.setSource(qUrl)

# hook required Slots
root = qView.rootObject()

# hook the safely quit command
root.safeQuit.connect(safelyQuitPlease)

# to timer and Cancel Button
cancelTweet = root.findChild(QObject, "cancelTweet")
cancelTweet.clicked.connect(safelyQuitPlease)

# add submit tweet signal
root.submitTweet.connect(submitedTweet)

# Show, Exit
qView.show()
sys.exit(qApp.exec_())
