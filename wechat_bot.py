# coding=utf8
import json
import os
import sys

import itchat
import requests

try:
    with open('tuling.json') as f:
        key = json.loads(f.read())['key']
except:
    key = ''  # if key is '', get_response will return None
    # raise Exception('There is something wrong with the format of you plugin/config/tuling.json')


def get_response(msg, storageClass=None, userName=None, userid='ItChat'):
    url = 'http://www.tuling123.com/openapi/api'
    payloads = {
        'key': key,
        'info': msg,
        'userid': userid,
    }
    try:
        r = requests.post(url, data=json.dumps(payloads)).json()
    except:
        return
    if not r['code'] in (100000, 200000, 302000, 308000, 313000, 314000):
        return
    if r['code'] == 100000:  # 文本类
        return '\n'.join([r['text'].replace('<br>', '\n')])
    elif r['code'] == 200000:  # 链接类
        return '\n'.join([r['text'].replace('<br>', '\n'), r['url']])
    elif r['code'] == 302000:  # 新闻类
        l = [r['text'].replace('<br>', '\n')]
        for n in r['list']:
            l.append('%s - %s' % (n['article'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 308000:  # 菜谱类
        l = [r['text'].replace('<br>', '\n')]
        for n in r['list']:
            l.append('%s - %s' % (n['name'], n['detailurl']))
        return '\n'.join(l)
    elif r['code'] == 313000:  # 儿歌类
        return '\n'.join([r['text'].replace('<br>', '\n')])
    elif r['code'] == 314000:  # 诗词类
        return '\n'.join([r['text'].replace('<br>', '\n')])


@itchat.msg_register('Text')
def text_reply(msg):
    if u'作者' in msg['Text'] or u'主人' in msg['Text']:
        return u'你可以在这里了解他：https://github.com/littlecodersh'
    elif u'源代码' in msg['Text'] or u'获取文件' in msg['Text']:
        itchat.send('@fil@main.py', msg['FromUserName'])
        return u'这就是现在机器人后台的代码，是不是很简单呢？'
    elif u'获取图片' in msg['Text']:
        # there should be a picture
        itchat.send('@img@applaud.gif', msg['FromUserName'])
    else:
        return get_response(msg['Text']) or u'收到：' + msg['Text']


@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({'Picture': u'图片', 'Recording': u'录音',
             'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
            u'已下载到本地')  # download function is: msg['Text'](msg['FileName'])


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'收到位置分享'
    elif msg['Type'] == 'Sharing':
        return u'收到分享' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'收到：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'收到好友信息：' + msg['Text']['Alias']


@itchat.msg_register('Text', isGroupChat=True)
def group_reply(msg):
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],
                                 get_response(msg['Text']) or u'收到：' + msg['Text'])


@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'项目主页：github.com/littlecodersh/ItChat\n'
                    + u'源代码  ：回复源代码\n' + u'图片获取：回复获取图片\n'
                    + u'欢迎Star我的项目关注更新！', msg['RecommendInfo']['UserName'])


itchat.auto_login(True, enableCmdQR=2)
itchat.run()
