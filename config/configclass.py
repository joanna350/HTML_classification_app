from config.singleton import singleton


@singleton
class ConfigClass:

    def __init__(self):
        self.config = dict()
        self.config_seed = None
        self.run = dict()

    def set_configuration(self, config, config_seed):
        self.config = config
        self.config_seed = config_seed
