from conf.config import MAX_NUM


class CacheData:
    def __init__(self):
        self.data = []
        self.row_id = 0

    def add_data(self, data):
        self.data.extend(data)
        self.data = self.data[-MAX_NUM:]  # 取最后 MAX_NUM 条数据


cache_obj = CacheData()
