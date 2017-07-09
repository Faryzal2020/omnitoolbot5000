from time import time
import pyrebase
from message import MessageApi

config = {
  "apiKey": " AIzaSyATH77v-A2RrmJfJXYQRFE0NRa4vzAObhU",
  "authDomain": "pybot2017.firebaseapp.com",
  "databaseURL": "https://pybot2017.firebaseio.com/",
  "storageBucket": "pybot2017.appspot.com"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

class Reminder:
	def __init__(self, message_api=None):
		if message_api == None:
			message_api = MessageApi()

		self.message_api = message_api

	def createReminder(self, username, userid, typeid, duration, msg, sourcetype):
		expiretime = int(time()) + duration
		expire = str(expiretime)
		data = {'expire':expire, 'username':username, 'userid':userid, 'typeid':typeid, 'message':msg, 'stype':sourcetype}
		db.child("reminders").child(expire).set(data)
		all_data = db.child("reminders").get()
		print(all_data.val())

	def checkExpiry(self):
		current = int(time())
		datas = db.child("reminders").get()
		if datas.each() != None:
			for data in datas.each():
				#print('KEY: ', data.key())
				#print('DATA: ', data.val())
				expire = data.val().get('expire')
				#print('EXPIRE: ', expire)
				#print('CURRENT: ', current)
				expireint = int(expire)
				if int(expireint) <= current:
					print("EXPIRE")
					username = data.val().get('username')
					userid = data.val().get('userid')
					typeid = data.val().get('typeid')
					msg = data.val().get('message')
					sourcetype = data.val().get('stype')
					db.child("reminders").child(expire).remove()
					self.message_api.send_text_message(username, userid, typeid, msg, sourcetype)
				break

