#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# author:Samray <samrayleung@gmail.com>

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import Flask, jsonify, request

deepThought = ChatBot("deepThought")
deepThought.set_trainer(ChatterBotCorpusTrainer)
# 使用中文语料库训练它
deepThought.train("chatterbot.corpus.chinese")  # 语料库
app = Flask(__name__)


@app.route("/chatbot")
def get_response():
    user_input = request.args.get('user_input')
    response = {}
    response['reply'] = deepThought.get_response(user_input).text
    return jsonify(response)


if __name__ == "__main__":
    app.run()
