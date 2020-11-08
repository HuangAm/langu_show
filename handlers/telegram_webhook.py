import json
import os
import subprocess

import requests
import tornado.web

from conf.config import PLF, CHART_JSON_PATH, CHART_EXPORT_CMD, IMG_DIR, MAX_NUM
from conf.log_conf import get_logger
from models import db_handler
from utils.common import data_resample, CJsonEncoder
from utils.short_id import get_short_id
from utils.telegram_api2 import BlueTest

logger = get_logger(__file__)


class TelegramWebHookHandler(tornado.web.RequestHandler):

    def initialize(self):
        self.bt = BlueTest()

    def get(self):
        self.post()

    def post(self):
        jsonbyte = self.request.body
        jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
        logger.info("json_str %s", jsonstr)
        if len(jsonstr) == 0:
            logger.warning('jsonstr is None')
            return
        jsonobj = json.loads(jsonstr)
        message = jsonobj['message']
        chat = message['chat']
        id = chat['id']
        text = message.get('text', '')
        if text == '/img':
            self.send_img(id)
        self.write("OK")

    def send_img(self, chat_id):
        logger.info("send_img entry")
        png_name = self.generate_png()
        # https://bluevallis.xiaojinlicai.com/jinzha/static/img/12a8982049e8852cc0e53e549a1ac83f.png
        logger.info("png_name %s", png_name)
        full_path = "/data/product/langu_show/static/img/" + png_name
        logger.info("full_path %s", full_path)
        self.upload_file(full_path)
        photo_url = 'http://test.010qu.com/data/%s' % png_name
        logger.info("photo_url %s", photo_url)
        # photo_url = 'https://bluevallis.xiaojinlicai.com/jinzha/static/img/%s' % png_name
        print(photo_url)
        self.bt.send_photo(chat_id, photo_url)

    def upload_file(self, file_path):
        url = 'http://test.010qu.com/tools/fileup1.php'
        files = {'upfile': open(file_path, 'rb')}
        data = {}
        response = requests.post(url, files=files, data=data)
        print(response.text)

    def generate_png(self):
        '''
        调用phantomjs生成png
        :return:
        '''
        start_row_id = db_handler.get_last_row_id() - MAX_NUM
        data, _ = db_handler.query_net("select t.id, t.create_time, t.net_value from t_fund_net_his as t where id > %s" % start_row_id)
        data = data_resample(data, '1H')
        with open(CHART_JSON_PATH, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
        chart_info["series"][0]["data"] = data
        with open(CHART_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(chart_info, f, cls=CJsonEncoder)
        png_name = get_short_id() + '.png'
        png_path = os.path.join(IMG_DIR, png_name)
        if PLF == 'Windows':
            subprocess.run(CHART_EXPORT_CMD.format(CHART_JSON_PATH, png_path))
        elif PLF == 'Linux':
            subprocess.run(CHART_EXPORT_CMD.format(CHART_JSON_PATH, png_path), shell=True)
        else:
            logger.error('Does not support %s platform' % PLF)
        return png_name
