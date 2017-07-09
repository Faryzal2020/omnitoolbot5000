from linebot import LineBotApi
from linebot.models import *

CHANNEL_ACCESS_TOKEN = 'zu7O2qB8l2jrkux+RqIPLQbsBMldgBXylkr3VF40spIpOmMysXvqcvbXfUKwnsEwHbpVJnXl0REK0mvjr2nGUP7+0vSB0csb8sx0w47Ps6niF715J3EhF8DzO46P+26MLeG3oTTVy0HZENb46Cg8rQdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

class MessageApi():

	def send_text_message(self, name, userid, typeid, text, sourcetype):
		send_text_message(name, userid, typeid, text, sourcetype)

def send_text_message(name, userid, typeid, text, sourcetype):
	message = 'Reminding '+name+' to '+text
	if sourcetype == 'user':
		to = userid
	else:
		to = typeid
	line_bot_api.push_message(to,TextSendMessage(text=message))
