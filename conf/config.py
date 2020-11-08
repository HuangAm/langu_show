import os
import platform

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'log')
CHART_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chart.json')
IMG_DIR = os.path.join(BASE_DIR, 'static', 'img')
PLF = platform.system()
MAX_NUM = 10000
if PLF == 'Linux':
    BASE_URL = 'http://106.75.12.30/'
    DB_CONFIG = {'host': '10.10.110.110', 'port': 3306, 'user': 'account', 'passwd': '123456', 'db': 'account_db'}
    CHART_EXPORT_CMD = './phantomjs static/hjs/highcharts-convert.js -infile {} -outfile {} -scale 2.5 -width 500 -constr StockChart'
else:
    BASE_URL = 'http://127.0.0.1:8080/'
    DB_CONFIG = {'host': '127.0.0.1', 'port': 3306, 'user': 'root', 'passwd': 'root', 'db': 'db1'}
    CHART_EXPORT_CMD = 'phantomjs.exe static/hjs/highcharts-convert.js -infile {} -outfile {} -scale 2.5 -width 500 -constr StockChart'
