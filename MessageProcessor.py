import json
from collections import namedtuple
from json import JSONEncoder
import KeepAlive as KeepAliveMessage
import datetime
from types import SimpleNamespace


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

# class customKeepAliveMessageDecoder(keepAliveDict):
#     return namedtuple('X', keepAliveDict.keys())(*keepAliveDict.values())



def ConvertMessageToJson(self, message):
    #keepAlive = KeepAliveMessage.KeepAlive(2, datetime.datetime.now().timestamp(), "234abc")
    convertedJson = json.dumps(message, indent=4, cls=MessageEncoder)
    return convertedJson

def ConvertJsonToMessage(self, jsonToParse):
    convertedMessage = json.loads(jsonToParse, object_hook=lambda parameter_list: SimpleNamespace(**parameter_list))
    return convertedMessage
