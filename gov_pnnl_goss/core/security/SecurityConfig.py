
# security_config.py


class SecurityConfig:

    def __init__(self, manager_user: str, manager_password: str):
        self.manager_user = manager_user
        self.manager_password = manager_password

    def get_manager_user(self):
        # return "your_manager_user_here"
        return self.manager_user

    def get_manager_password(self):
        # return "your_manager_password_here"
        return self.manager_password

    def get_use_token(self):
        pass

    def validate_token(self, token):
        pass

    def parse_token(self, token):
        pass

    def create_token(self, user_id, roles):
        pass

    def get_class(self):
        pass
