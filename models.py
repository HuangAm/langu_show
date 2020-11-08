import traceback

import pymysql

from conf.config import DB_CONFIG
from conf.log_conf import get_logger

logger = get_logger(__file__)


class DBHandler:

    def __init__(self):
        self.conn = self.to_connect()

    def __del__(self):
        self.conn.close()

    def to_connect(self):
        return pymysql.connect(**DB_CONFIG)

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.conn.ping(reconnect=True)
        except:
            logger.error(traceback.print_exc())
            self.conn = self.to_connect()

    def get_last_row_id(self):
        self.is_connected()
        cursor = self.conn.cursor()

        cursor.execute('select count(id) from t_fund_net_his')
        row_id = cursor.fetchone()[0]
        self.conn.commit()
        cursor.close()
        return row_id

    def query_net(self, sql_str, last_row_id=0, cache=False):
        self.is_connected()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        data = []
        row_id = last_row_id
        for row in rows:
            data.append((row[1], row[2] / 100))
            row_id = row[0]
        self.conn.commit()
        cursor.close()
        return data, row_id


db_handler = DBHandler()
