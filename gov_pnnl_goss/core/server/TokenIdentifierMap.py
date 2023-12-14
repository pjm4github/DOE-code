
class TokenIdentifierMap:
    """
    * TokenIdentifierMap is a container of tokens that have been
    * authenticated with the user login service.
    *
    * @author Craig Allwardt
    """
    def __init__(self):
        self.token_map = {}

    def register_identifier(self, ip, identifier):
        self.token_map[ip] = identifier

    def register_identifier_with_token(self, ip, token, identifier):
        self.token_map[(ip, token)] = identifier

    def get_identifier(self, ip, token):
        return self.token_map.get((ip, token), None)
