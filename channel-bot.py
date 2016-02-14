# coding:utf-8
from slackclient import SlackClient
import time
import json
from ConfigParser import SafeConfigParser


def is_channels_command(res):
    return (res["type"] == "message") and ("text" in res) and (command == res["text"])


def is_channel_created_event(res):
    return res["type"] == "channel_created"


def convert_channels_to_text(channels):
    text_list = [u"チャンネル一覧:hatched_chick:\n"]
    for channel in channels["channels"]:
        purpose = channel["purpose"]
        line = channel["name"] + " : " + purpose["value"] + "\n\n"
        text_list.append(line)
    return "".join(text_list)


config = SafeConfigParser()
config.read("config.ini")
token = config.get("slack", "token")
command = config.get("slack", "command")
room = config.get("slack", "room")
sc = SlackClient(token)

if sc.rtm_connect():
    while True:
        response = sc.rtm_read()
        for res in response:
            print res
            if "type" in res:
                if is_channels_command(res):
                    channels = json.loads(sc.api_call("channels.list", exclude_archived="1"))
                    text = convert_channels_to_text(channels)
                    sc.rtm_send_message(room, text)
                    time.sleep(1)
                elif is_channel_created_event(res):
                    channel_info = res["channel"]
                    text = "New Channel!:sparkles:\n" + channel_info["name"]
                    sc.rtm_send_message(room, text)
                    time.sleep(1)
else:
    print "Connection Failed, invlalid token?"
