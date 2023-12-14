
# user_repository.py


class UserRepository:
    
    def find_by_user_id(self, user_id):
        pass
    
    def find_by_id(self, id):
        pass

    def generate_shared_key(self):
        # //    public byte[] generateSharedKey();
        pass

    def get_expiration_date(self):
        # //    public long getExpirationDate() ;
        pass

    def get_issuer(self):
        # //    public String getIssuer();
        pass

    def create_token(self, user):
        pass
        # //    public TokenResponse createToken(UserDefault user) ;
        #
        # //    public String createToken(Object userId) ;

    def validate_token(self, token):
        # //    public boolean validateToken(String token);
        pass