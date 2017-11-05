#!/usr/bin/env python
# coding: utf-8

import threading

#from wxbot import WXBot
import itchat
import requests
from itchat.content import TEXT

# todo 用另一个进程把服务起来
bot_api = "http://127.0.0.1:8000/get_response"

# 带对象参数注册，对应消息对象将调用该方法


@itchat.msg_register(TEXT, isFriendChat=True)
def text_reply(msg):
    user_input = msg['Text']
    payload = {"user_input": user_input}
    response = requests.get(bot_api, params=payload).json()["response"]
    itchat.send(response, msg['FromUserName'])


# 把服务跑起来 bottle
def bot_server():
    from bottle import Bottle, run
    from bottle import response, request
    from chatterbot import ChatBot
    from chatterbot.trainers import ChatterBotCorpusTrainer
    from json import dumps

    deepThought = ChatBot("deepThought")
    deepThought.set_trainer(ChatterBotCorpusTrainer)
    # 使用中文语料库训练它
    deepThought.train("chatterbot.corpus.chinese")  # 语料库

    app = Bottle()

    @app.route('/get_response')
    def get_response():
        user_input = request.query.user_input or ""
        d_response = deepThought.get_response(user_input).text
        response.content_type = 'application/json'
        res = {"response": d_response}
        return dumps(res)

    run(app, host='localhost', port=8000)


botThread = threading.Thread(target=bot_server)
botThread.setDaemon(True)
botThread.start()

itchat.auto_login(hotReload=True)
itchat.run()
