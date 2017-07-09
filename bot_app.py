import requests
import re
import wolframalpha as wf
from flask import Flask, request, abort

from googleapiclient.discovery import build

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

from reminder import Reminder

CHANNEL_ACCESS_TOKEN = 'zu7O2qB8l2jrkux+RqIPLQbsBMldgBXylkr3VF40spIpOmMysXvqcvbXfUKwnsEwHbpVJnXl0REK0mvjr2nGUP7+0vSB0csb8sx0w47Ps6niF715J3EhF8DzO46P+26MLeG3oTTVy0HZENb46Cg8rQdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = '627b4f46b5dd310fad9bc466761f3280'

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
wfclient = wf.Client('TJL6V6-UT5632ARJR')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def wolfram(queryText):
    i = 0
    result = ''
    res = wfclient.query(queryText)
    if queryText == ' ':
        result = 'Usage: wf <query> \n Query hanya bisa dalam bahasa inggris \n Contoh: wf 6th US president'
    else:
        for pod in res.pods:
            i += 1
            if i == 2:
                for sub in pod.subpods:
                    result += sub['plaintext']
    return result

def tokopedia(queryText):
    service = build("customsearch", "v1", developerKey="AIzaSyA9u11EUgVxfFdPTe9LeFVG2501obcPEUY")
    result = service.cse().list(q=queryText, cx='006613523229680227918:m7epsqbcask').execute()
    return result

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("Event: ", event)
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    rem = Reminder()
    
    if event.source.type == 'user':
        userid = event.source.user_id
        typeid = ''
        sourcetype = 'user'
    elif event.source.type == 'group':
        userid = event.source.user_id
        typeid = event.source.group_id
        sourcetype = 'group'
    elif event.source.type == 'room':
        userid = event.source.user_id
        typeid = event.source.room_id
        sourcetype = 'group'

    try:
        profile = line_bot_api.get_profile(userid)
        username = profile.display_name
    except LineBotApiError:
        userid = typeid
        username = 'someone in this group'

    replyToken = event.reply_token
    text = event.message.text
    if text.count(' ') > 0:
        command,message = text.split(' ', 1)
    else:
        command = text
        message = ' '

    print("command:", command)
    print("message:", message)

    if command == "/wf":
        try:
            content = wolfram(message)
        except AttributeError:
            content = 'invalid query'
        line_bot_api.reply_message(
            replyToken,
            TextSendMessage(text=content))

    elif command == "/tp":
        res = tokopedia(message)
        data = res.get('items')[0].get('pagemap').get('metatags')[0]
        if data.get('twitter:data1') is not None:
            msg = []
            judul, a = data.get('og:title').split('|', 1)
            textt = 'Harga: '+data.get('twitter:data1')+'\nKota: '+data.get('twitter:data2')+'\n\n'+data.get('og:url')
            msg.append(TextSendMessage(text=judul))
            msg.append(ImageSendMessage(
                original_content_url=data.get('og:image'),
                preview_image_url=data.get('og:image')))
            msg.append(TextSendMessage(text=textt))
            print('MESSAGE: ', msg[0].text)
            line_bot_api.reply_message(replyToken,msg)
        else:
            line_bot_api.reply_message(replyToken,TextSendMessage(text="Nama barang yang dicari terlalu umum / kurang detail"))

    elif command == "/remind":
        # me to <do stuff> in <x> <time>
        m = re.search('me to(\s.+)(?=in)(in\s)(\d+)(\s\w+)', message)

        if m != None:
            msg = m.group(1).strip()
            time1 = int(m.group(3))
            time2 = m.group(4)
            print('time2= ',time2)
            time = 0
            if time1 > 0:
                if time2 == ' minute' or time2 == ' minutes':
                    time = time1*60
                elif time2 == ' hour' or time2 == ' hours':
                    time = time1*3600
                elif time2 == ' day' or time2 == ' days':
                    time = time1*86400
                elif time2 == ' week' or time2 == ' weeks':
                    time = time1*604800
                printt = 'TIME= '+str(time)+' seconds'
                print(printt)
                rem.createReminder(username, userid, typeid, time, msg, sourcetype)

                line_bot_api.reply_message(
                    replyToken,
                    TextSendMessage(text='ok'))
        else:
            line_bot_api.reply_message(
                replyToken,
                TextSendMessage(text='your command is invalid'))

    elif text == "/test":
        content = 'hello, '+username+'. \nyour userid is ' + userid
        line_bot_api.reply_message(
            replyToken,
            TextSendMessage(text=content))

    else:
        line = []
        line.append('Daftar fungsi yang bisa digunakan: \n\n')
        line.append('Wolfram: Mencari informasi umum, menyelesaikan perhitungan, mencari definisi, dll.\n')
        line.append('   Command: "/wf <query>"\n')
        line.append('   Query harus dalam bahasa inggris dan jelas. \n')
        line.append('   contoh: "/wf us third president"\n\n')
        line.append('Tokopedia: Mencari barang yang dijual di tokopedia sesuai query.\n')
        line.append('   Command: "/tp <query>"\n')
        line.append('   Query tidak boleh menggunakan kata yang terlalu umum. \n')
        line.append('   contoh: "/tp gtx 1050"\n\n')
        line.append('Reminder: Meminta bot untuk mengirim pesan yang diinginkan setelah waktu yang ditentukan\n')
        line.append('   Command: "/remind me to <message> in <angka> <satuanWaktu>"\n')
        line.append('   Satuan waktu yang bisa digunakan mulai dari minute(s) sampai week(s)\n')
        line.append('   contoh: "/remind me to ngerjain tugas python in 3 hours"\n')
        content = '-'.join(line)

        if sourcetype == 'user' or text == '/help':
            line_bot_api.reply_message(
                replyToken,
                TextSendMessage(text=content))

if __name__ == '__main__':
    app.run(debug=true)