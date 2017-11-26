#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# author:Samray <samrayleung@gmail.com>
import pdb
import sqlite3
import time

# 使用微软的小冰作为智能回复的 AI, 因为微软没有开放小冰的 api, 但是有接入到微博
# 和微信平台，所以就要利用微信公众号接口调用小冰
import itchat
from db import DatabaseManager, insert_text_message
from itchat.content import (ATTACHMENT, CARD, MAP, NOTE, PICTURE, RECORDING,
                            SHARING, TEXT, VIDEO)
from manager import db_filename, schema_filename

global name
dbmgr = DatabaseManager(db_filename, schema_filename)
"""
def msg_register(self, msgType,
        isFriendChat=False, isGroupChat=False, isMpChat=False):
    ''' a decorator constructor
        return a specific decorator based on information given
    '''
"""
"""
def send(self, msg, toUserName=None, mediaId=None):
    ''' wrapped function for all the sending functions
        for options
            - msg: message starts with different string indicates different type
                - list of type string: ['@fil@', '@img@', '@msg@', '@vid@']
                - they are for file, image, plain text, video
                - if none of them matches, it will be sent like plain text
            - toUserName: 'UserName' key of friend dict
            - mediaId: if set, uploading will not be repeated
        it is defined in components/messages.py
    '''
    raise NotImplementedError()
"""


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], True, False, False)
#  将文字等信息转发给小冰
def send_xiaoice(msg):
    # 保存对话到数据库
    insert_text_message(db_filename, msg)
    global name
    name = msg['FromUserName']
    xb = itchat.search_mps(name='小冰')[0]
    print("{}: ".format(name), msg['Text'])
    itchat.send(msg['Text'], xb['UserName'])


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], True, False, False)
# 将图片等信息转发给小冰
def send_xiaoice(msg):
    global name
    name = msg['FromUserName']
    msg['Text'](msg['FileName'])
    xb = itchat.search_mps(name='小冰')[0]
    print("{}: send you a pitcure".format(name))
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(
        msg['Type'], 'fil'), msg['FileName']), xb['UserName'])


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], False, False, True)
# 将小冰回复的文字等信息转发给发送者
def send_reply(msg):
    insert_text_message(db_filename, msg)
    global name
    print("xiaoice reply: ", msg['Text'])
    itchat.send(msg['Text'], name)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], False, False, True)
# 将小冰回复的图片等信息转发给发送者
def send_reply(msg):
    global name
    msg['Text'](msg['FileName'])
    itchat.send('@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(
        msg['Type'], 'fil'), msg['FileName']), name)


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u' 就知道你想勾搭我', msg['RecommendInfo']['UserName'])


itchat.auto_login(enableCmdQR=2)
itchat.run()
