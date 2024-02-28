import logging


def log_output(name='root',
               logger_level='DEBUG',
               stream_handler_level='DEBUG',
               filename=None,
               file_handler_level='DEBUG',
               fmt='%(asctime)s---%(filename)s---[line:%(lineno)d]---%(levelname)s:%(message)s'
               ):
    # 得到收集器，设置等级
    logger = logging.getLogger(name)
    logger.setLevel(logger_level)
    # 流管理器
    stream_handler = logging.StreamHandler()
    # 设置等级
    stream_handler.setLevel(stream_handler_level)
    # 绑定
    logger.addHandler(stream_handler)
    # 设置格式，添加格式
    fmt = logging.Formatter(fmt)
    stream_handler.setFormatter(fmt)
    # 如果参数传了filename，则日志输出到filename的路径
    if filename:
        file_handler = logging.FileHandler(filename, encoding='utf8')
        file_handler.setLevel(file_handler_level)
        logger.addHandler(file_handler)
        file_handler.setFormatter(fmt)
    return logger



