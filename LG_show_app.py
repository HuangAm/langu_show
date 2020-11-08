import json
import os
import subprocess

import tornado.ioloop
import tornado.web

from conf.cache_conf import cache_obj
from conf.config import BASE_URL, PLF, CHART_JSON_PATH, CHART_EXPORT_CMD, IMG_DIR, MAX_NUM
from conf.log_conf import get_logger
from handlers.telegram_webhook import TelegramWebHookHandler
from models import db_handler
from utils.common import CJsonEncoder, data_resample
from utils.short_id import get_short_id

logger = get_logger(__file__)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class LGShowHandler(tornado.web.RequestHandler):
    def get(self):
        last_row_id = self.get_argument('rowId', None)
        freq = self.get_argument('freq', None)
        if not last_row_id or last_row_id == '0':
            if len(cache_obj.data) == 0:  # 初次请求且缓存中没有数据，查询表中最后 10000 条数据
                start_row_id = db_handler.get_last_row_id() - MAX_NUM
                data, row_id = db_handler.query_net("select t.id, t.create_time, t.net_value from t_fund_net_his as t where id > %s" % start_row_id)
                # 将数据更新到 CacheData
                cache_obj.data = data
                cache_obj.row_id = row_id
        else:
            # 每分钟请求时用上次放回的 last_row_id 查询最新数据
            data, row_id = db_handler.query_net("select t.id, t.create_time, t.net_value from t_fund_net_his as t where id > %s" % last_row_id, last_row_id)
            if len(data) != 0:
                cache_obj.add_data(data)
                cache_obj.row_id = row_id
        if not freq or freq == '1T':  # 如果是未传入 freq 参数或者 freq = '1T' 用原始数据（即分钟数据）
            data = cache_obj.data
        else:  # 其余情况进行重采样，这里未作 freq 传入其他参数报错的情况
            data = data_resample(cache_obj.data, freq)
        row_id = cache_obj.row_id
        self.write(json.dumps({"data": data[-720:], "rowId": row_id}, cls=CJsonEncoder))


class ExportHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
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
            self.write('Does not support %s platform' % PLF)
            logger.error('Does not support %s platform' % PLF)
            return
        png_url_path = BASE_URL + '/'.join(['static', 'img', png_name])
        self.redirect(png_url_path)


def make_app():
    settings = {
        'template_path': 'templates',
        'static_path': 'static',
        'static_url_prefix': '/static/',
    }
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/data/", LGShowHandler),
        (r"/export/", ExportHandler),
        (r"/webhook/", TelegramWebHookHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
