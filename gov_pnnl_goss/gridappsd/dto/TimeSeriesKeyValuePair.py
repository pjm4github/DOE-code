
class TimeSeriesKeyValuePair:
    def __init__(self):
        self.key_value_pair = {}

    def get_key_value_pair(self):
        return self.key_value_pair

    def set_key_value_pair(self, key_value_pair):
        self.key_value_pair = key_value_pair

    def get_value(self, key):
        return self.key_value_pair.get(key)
