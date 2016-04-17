# coding:utf-8
from slackclient import SlackClient
import time
import json
from ConfigParser import SafeConfigParser


def is_channels_message(res, channel_list):
    if not "channel" in res:
        return False
    exist_list = [channel for channel in channel_list if res["channel"] == channel["id"]]
    return (res["type"] == "message") and exist_list and ("text" in res) and (command == res["text"])


def is_channel_created_event(res):
    return res["type"] == "channel_created"


def is_direct_message(res, im_list):
    if not "channel" in res:
        return False
    exist_list = [im for im in im_list if res["channel"] == im["id"]]
    return (res["type"] == "message") and exist_list and ("text" in res) and (command == res["text"])


def convert_channels_to_text(channels):
    text_list = [u"チャンネル一覧:hatched_chick:\n"]
    for channel in channels["channels"]:
        purpose = channel["purpose"]
        line = "#" + channel["name"] + " : " + purpose["value"]+ "\n\n"
        text_list.append(line)
    return "".join(text_list).encode("utf-8")


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
                if is_channels_message(res, json.loads(sc.api_call("channels.list", exclude_archived="1"))["channels"]):
                    channels = json.loads(sc.api_call("channels.list", exclude_archived="1"))
                    text = convert_channels_to_text(channels)
                    sc.api_call("chat.postMessage", channel=room, text=text, link_names="1", as_user="1")
                    time.sleep(1)
                elif is_channel_created_event(res):
                    channel_info = res["channel"]
                    text = "New Channel!:sparkles:\n" + "#" + channel_info["name"]
                    sc.api_call("chat.postMessage", channel=room, text=text, link_names="1", as_user="1")
                    time.sleep(1)
                elif is_direct_message(res, json.loads(sc.api_call("im.list"))["ims"]):
                    channels = json.loads(sc.api_call("channels.list", exclude_archived="1"))
                    text = convert_channels_to_text(channels)
                    sc.api_call("chat.postMessage", channel=res["channel"], text=text, link_names="1", as_user="1")
                    time.sleep(1)
else:
    print "Connection Failed, invlalid token?"
