# channel-bot
Slackの中のチャンネル情報を通知してくれるbotです。  
以下のことができます。

- 指定した文字列が打ち込まれるとチャンネル一覧を表示する
- 新しいチャンネルが作成されると、チャンネル名を通知する

[pyton-slackclient](https://github.com/slackhq/python-slackclient)を使用しています。


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
command ・・・ここで指定した文字列を含むメッセージがSlack内で使用されると特定のチャンネルに現在のチャンネル一覧が表示されます  
room ・・・通知を行いたいSlackのルーム名を指定します(トークンの持ち主が所属するルームである必要があります)
  
スクリプトを実行し、botを立ち上げます
```
$ python channel-bot.py
```
