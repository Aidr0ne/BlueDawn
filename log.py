from control import app

from logzero import logger as l # type: ignore
import logzero

@app.register_class
class logger:
    def __init__(self, config=None, log_config=False, log_fc=False): 
        self.config = config
        logzero.logfile("/tmp/log.log")
        if log_config:
            self.log_config()
        if log_fc:
            self.log_fc()

    def log_array(self, items):
        if isinstance(items, dict):
            for key, value in items.items():
                if isinstance(value, (dict, list)):
                    self.log_array(value)
                else:
                    l.info(f"{key}: {value}")
        elif isinstance(items, list):
            for i, value in enumerate(items):
                if isinstance(value, (dict, list)):
                    self.log_array(value)
                else:
                    l.info(f"[{i}]: {value}")

    def log_config(self):
        l.info("##########################################CONFIG##########################################")
        self.log_array(self.config)

    def log_fc(self):
        l.info("##########################################CLASS'S#########################################")
        self.log_array(app.class_list)
        l.info("#########################################FUNCTIONS########################################")
        self.log_array(app.function_list)

    def info(self, item):
        l.info(str(item))

    def debug(self, item):
        l.debug(item)
