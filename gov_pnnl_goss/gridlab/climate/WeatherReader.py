
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106

class RECORDS:
    def __init__(self, low=None, low_day=None, high=None, high_day=None, solar=None):
        self.low = low
        self.low_day = low_day
        self.high = high
        self.high_day = high_day
        self.solar = solar

class WeatherReader:
    def __init__(self):
        self.infile = 0
        self.data_head = 0
        self.data_tail = 0
