import requests
import re
import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
line_bot_api = LineBotApi('zu7O2qB8l2jrkux+RqIPLQbsBMldgBXylkr3VF40spIpOmMysXvqcvbXfUKwnsEwHbpVJnXl0REK0mvjr2nGUP7+0vSB0csb8sx0w47Ps6niF715J3EhF8DzO46P+26MLeG3oTTVy0HZENb46Cg8rQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('627b4f46b5dd310fad9bc466761f3280')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    a,b = event.message.text.split(' ', 1)
    if a == "try":
        content = b
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    if a == "help":
        content = 'wwwwwwww'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    

if __name__ == '__main__':
    app.run()