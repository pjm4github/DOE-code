# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class BgResult:
    
    def __init__(self, s, p, o):
        self.subject = s
        self.property = p
        self.object = o

    def get_subject(self):
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    def get_property(self):
        return self.property

    def set_property(self, property):
        self.property = property

    def get_object(self):
        return self.object

    def set_object(self, object):
        self.object = object
