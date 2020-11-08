import json
from datetime import datetime

import pandas as pd


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.tz_localize('Asia/Shanghai').timestamp() * 1000
        elif isinstance(obj, datetime):
            return obj.timestamp() * 1000
        else:
            return json.JSONEncoder.default(self, obj)


def data_resample(data, freq):
    df = pd.DataFrame(data=data, columns=['date', 'net'])
    df.set_index(df['date'], inplace=True)
    df = df.resample(freq).apply(lambda arr: arr[-1])
    return df.values.tolist()
