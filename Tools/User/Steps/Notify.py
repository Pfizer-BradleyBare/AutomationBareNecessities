from ..Steps import Steps as STEPS
from ...Hamilton.Commands import Notify as NOTIFY
from ...General import Log as LOG

TITLE = "Notify"
WAIT_ON_USER = "Wait On User"
SUBJECT = "Subject"
MESSAGE = "Message"

IsUsedFlag = True

def IsUsed():
	global IsUsedFlag
	return IsUsedFlag

def Init():
	pass

def Step(step):
	LOG.Step(step)
	Parameters = step.GetParameters()
	NOTIFY.SendMessage(Parameters[WAIT_ON_USER],Parameters[SUBJECT],Parameters[MESSAGE])