# channel-bot
Slackの中のチャンネル情報を通知してくれるbotです。  
以下のことができます。

- 指定した文字列が打ち込まれるとチャンネル一覧を表示する
- 新しいチャンネルが作成されると、チャンネル名を通知する

Slackの[Real Time Messaging API](https://api.slack.com/rtm)を使用しており、
ライブラリとして[pyton-slackclient](https://github.com/slackhq/python-slackclient)を使用しています。


# Installation
Githubからクローンしてきます
```
$ git clone https://github.com/ymym3412/channel-bot
```
```
$ cd channel-bot
```
  
ライブラリのインストールを行います
```
$ pip install -r requirements.txt
```

# Usage
confgi.iniに必要な情報を記述します
```
token={your slack token or bot token}
command={show all channels}
room={room name that you want to nortificate like general}
```
token ・・・ユーザーのtoken、あるいはbot用のトークンを指定します  
command ・・・ここで指定した文字列を含むメッセージが特定のチャンネルなどで使用されると指定したチャンネルに現在のチャンネル一覧が表示されます  
room ・・・通知を行いたいSlackのチャンネル名を指定します(トークンの持ち主が所属するチャンネルである必要があります)
  
スクリプトを実行し、botを立ち上げます。
```
$ python channel-bot.py
```
`config.ini`でbot用のtokenを使用した場合は、そのbotを`config.ini`のroomで指定したroomに招待してください。

# Example
## チャンネル一覧の表示
`config.ini`の`command`で指定した文字列がroomで指定したチャンネルで使用されると、チャンネルの一覧が表示されます。
### 「channels」を指定した場合
```
user:channels
bot:チャンネル一覧
    general
    random
    sample-room
```

## 新しく作成されたチャンネルの通知
Slack内で新しいチャンネルが作成されると、指定されたチャンネルに通知が飛びます。
```
bot:New Channel!
    new-channel-name
```
