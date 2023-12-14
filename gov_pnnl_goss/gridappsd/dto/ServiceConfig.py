
class ServiceConfig:
    serial_version_UID = -2413334775260242364
    def __init__(self):
        self.id = None
        self.user_options = {}
        self.user_value = None

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_user_options(self):
        return self.user_options

    def set_user_options(self, user_options):
        self.user_options = user_options
