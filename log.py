from logzero import logger as l # type: ignore
import logzero

class logger:
    def __init__(self, config=None, log_config=False): 
        self.config = config
        logzero.logfile("/tmp/log.log")
        l.debug("hello")
        if log_config:
            self.log_config()

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
        self.log_array(self.config)

    def info(self, item):
        l.info(str(item))
