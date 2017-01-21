# coding:utf-8
import os
import sys
import time
import json
from ConfigParser import SafeConfigParser, MissingSectionHeaderError

from slackclient import SlackClient
from logbook import Logger
from logbook import RotatingFileHandler
from logbook import StreamHandler

logger = Logger("channel-bot")


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


def is_emoji_changed_event(res):
    return res["type"] == "emoji_changed" and res["subtype"] == "add"


def convert_channels_to_text(channels):
    text_list = [u"チャンネル一覧:hatched_chick:\n"]
    for channel in channels["channels"]:
        purpose = channel["purpose"]
        line = "#" + channel["name"] + " : " + channel["name"] + " : " + purpose["value"]+ "\n\n"
        text_list.append(line)
    return "".join(text_list).encode("utf-8")


def setup_logger(config):
    if config.has_option("slack", "log_output"):
        output_path = config.get("slack", "log_output")
        dir_path, file_name = os.path.split(output_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_handler = RotatingFileHandler(output_path, backup_count=5)
        file_handler.push_application()
    else:
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.push_application()


def read_config(config):
    error_message = "Please create 'slack' section and contain options."
    try:
        config.read("config.ini")
    except MissingSectionHeaderError:
        print error_message
        exit()

    if not config.has_section("slack"):
        print error_message
        exit()


def parse_required_option(config, option):
    if not config.has_option("slack", option):
        print "Please setting '{}' option in {} section.".format(option, "slack")
        exit()

    return config.get("slack", option)


config = SafeConfigParser()
read_config(config)
token = parse_required_option(config, "token")
command = parse_required_option(config, "command")
room = parse_required_option(config, "room")
setup_logger(config)
sc = SlackClient(token)

if sc.rtm_connect():
    logger.info("channel-bot is up")

    while True:
        response = sc.rtm_read()
        for res in response:
            logger.info(res)
            if "type" in res:
                if is_channels_message(res, json.loads(sc.api_call("channels.list", exclude_archived="1"))["channels"]):
                    channels = json.loads(sc.api_call("channels.list", exclude_archived="1"))
                    text = convert_channels_to_text(channels)
                    sc.api_call("chat.postMessage", channel=room, text=text, link_names="1", as_user="1")
                    time.sleep(1)
                elif is_channel_created_event(res):
                    channel = res["channel"]
                    time.sleep(2)
                    channel_info = json.loads(sc.api_call("channels.info", channel=channel["id"]))
                    text = "New Channel!:sparkles:\n" + "#" + channel["name"] + " : " + channel["name"] + " : " + channel_info["channel"]["purpose"]["value"]
                    sc.api_call("chat.postMessage", channel=room, text=text.encode("utf-8"), link_names="1", as_user="1")
                    time.sleep(1)
                elif is_direct_message(res, json.loads(sc.api_call("im.list"))["ims"]):
                    channels = json.loads(sc.api_call("channels.list", exclude_archived="1"))
                    text = convert_channels_to_text(channels)
                    sc.api_call("chat.postMessage", channel=res["channel"], text=text, link_names="1", as_user="1")
                    time.sleep(1)
                elif is_emoji_changed_event(res):
                    text = "New Stamp!`:{}:`:sparkles:\nOriginal: {}".format(res["name"], res["value"])
                    sc.api_call("chat.postMessage", channel=room, text=text, as_user="1")

else:
    logger.critical("Connection Failed, invalid token?")
