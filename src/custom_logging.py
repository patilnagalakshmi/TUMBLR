'''To create custom logging'''
import logging
def setup_logger(log_file='log/Tumblr',level=logging.DEBUG):
    '''To create setup_logger'''
    logger = logging.getLogger('__TUMBLR__')
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s-%(name)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
loggers=setup_logger()
