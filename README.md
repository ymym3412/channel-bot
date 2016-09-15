# channel-bot
Slackの中のチャンネル情報を通知してくれるbotです。  
以下のことができます。

- 指定した文字列が打ち込まれるとチャンネル一覧を表示する
- 新しいチャンネルが作成されると、チャンネル名を通知する
- 新しいemojiが追加されると、チャンネルに通知する

チャンネル一覧と新しいチャンネル通知はリンクとして表示されるため、すぐにそのチャンネルを見に行くことができます。
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
config.iniに必要な情報を記述します
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
`config.ini`の`command`で指定した文字列がroomで指定したチャンネルで使用されると、チャンネルの一覧と各チャンネルのpurposeが表示されます。  
アーカイブされたチャンネルは表示されません。またチャンネル名はリンクとして表示されます。
### 「channels」を指定した場合
```
user:channels
bot:チャンネル一覧
    #general : This channel is for team-wide...

    #random : A place for non-work banter, links, articles ...
    
    #sample-room : {purpose of sample-room}
```

## 新しく作成されたチャンネルの通知
Slack内で新しいチャンネルが作成されると、指定されたチャンネルに通知が飛びます。  
チャンネル名はリンクとして表示されます。
```
bot:New Channel!
    #new-channel-name
```

## 新しく追加されたemojiの通知
Slackに新しいemojiが追加されると、emoji名とオリジナルのファイルを表示します。
```
bot:New Stamp!`:zoi:`
    Original: https://emoji.slack-edge.com/T03JDMZLZ/zoi1/c3e... 
```
