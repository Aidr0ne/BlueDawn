class App:
    def __init__(self):
        self.function_list = []
        self.class_list = []

    def register_function(self, func):
        self.function_list.append(func.__name__)
        return func

    def register_class(self, cls):
        self.class_list.append(cls.__name__)
        return cls

app = App()