
class environment_variable:
    def __init__(self):
        self.env_name = None
        self.env_value = None

    def get_env_name(self):
        return self.env_name

    def set_env_name(self, env_name):
        self.env_name = env_name

    def get_env_value(self):
        return self.env_value

    def set_env_value(self, env_value):
        self.env_value = env_value
