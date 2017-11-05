from __future__ import unicode_literals

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

deepThought = ChatBot("Training demo")
deepThought.set_trainer(ListTrainer)
deepThought.train([
    "嗳，渡边君，真喜欢我?",
    "那还用说?",
    "那么，可依得我两件事?",
    "三件也依得",
])


# test
print(deepThought.get_response("真喜欢我?"))
print(deepThought.get_response("可依得我两件事?"))
