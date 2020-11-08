'''
Done! Congratulations on your new bot.
You will find it at t.me/bluetest1_bot.
 You can now add a description, about section and profile picture for your bot,
 see /help for a list of commands. By the way, when you've finished creating your cool bot,
  ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
1388349603:AAGgM720ALZ-vl-4uiQEXIbuXp9fOdtyTRY
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api

'''
import requests
import json


class BlueTest:
    def __init__(self):
        self.base_url = 'https://api.telegram.org/bot1388349603:AAGgM720ALZ-vl-4uiQEXIbuXp9fOdtyTRY'

    def work(self):
        pass

    def send_photo(self, chat_id, photo_url):
        '''
        https://core.telegram.org/bots/api#sendphoto
        '''
        method_name = 'sendPhoto'
        json_data = {'chat_id': chat_id, "photo": photo_url}
        self.send_proxy(method_name, json_data)

    def getUpdates(self):
        method_name = 'getUpdates'
        json_data = {'play_boy': '123456'}
        return self.send_proxy(method_name, json_data)

    def send_proxy(self, metond_name, req_json_data):
        url = 'http://test.010qu.com/tools/telgram2.php'
        response = requests.post(url=url, data={'method_name': metond_name, 'json_data': json.dumps(req_json_data)})
        resp = response.text
        content = resp.encode('utf-8').decode('unicode_escape')
        print(content)
        return content

    def get_me(self):
        method_name = 'getMe'
        json_data = {'play_boy': '123456'}
        return self.send_proxy(method_name, json_data)

    def setWebhook(self):
        method_name = 'setWebhook'
        #json_data = {'url': 'https://bluevallis.xiaojinlicai.com/callback/callback/mybluetest1.do'}
        json_data = {'url': 'https://bluevallis.xiaojinlicai.com/jinzha/webhook/'}
        self.send_proxy(method_name, json_data)


if __name__ == '__main__':
    bt = BlueTest()

    # content = bt.getUpdates()
    # print(bt.get_me())

    # chat_id = 1165959848
    # # photo_url = 'https://img.tupianzj.com/uploads/allimg/202008/9999/d0745ebebe.jpg'
    # # photo_url = 'http://106.75.12.30/static/img/ef459f5e71cacf24d9ea7053005692a7.png'
    # photo_url = 'https://bluevallis.xiaojinlicai.com/callback/callback/jzpic.png'
    # bt.send_photo(chat_id, photo_url)

    bt.setWebhook()
