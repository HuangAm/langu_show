import logging
import os

from conf.config import LOG_DIR


def get_logger(log_name, filename='langu.log', level=logging.INFO):  # 每次用都写这么多太麻烦，直接定义一个函数，要改需求在函数里面改就好了
    logger = logging.getLogger(log_name)  # 实例化产生一个对象
    fm = logging.Formatter('%(asctime)s-%(name)s-%(lineno)d-%(levelname)s-%(message)s')  # 创建一个格式对象
    fh = logging.FileHandler(os.path.join(LOG_DIR, filename))  # 创建一个文件流handler(处理程序)，用于写入日志
    sh = logging.StreamHandler()  # 创建一个屏幕流，用于输出到控制台

    fh.setFormatter(fm)  # 文件流吸入格式对象，对象之间的交互
    sh.setFormatter(fm)  # 屏幕流吸入格式对象，对象之间的交互

    logger.addHandler(fh)  # 添加文件流，默认就是追加写
    logger.addHandler(sh)  # 添加屏幕流

    logger.setLevel(level)  # 设计等级只能对logger对象进行设置，fh和sh设计了不管用
    return logger
