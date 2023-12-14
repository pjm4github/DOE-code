
# from jose import JOSEException
# from jose.jwt import JWTClaimsSet
# from jose.jws import JWSHeader
# from jose.jws import MACVerifier
# from jose.utils import Base64URL
from datetime import date

from gov_pnnl_goss.SpecialClasses import MACVerifier


class MacVerifierExtended(MACVerifier):
    
    def __init__(self, shared_secret, claims_set) -> None:
        super().__init__(shared_secret)
        self.claims_set = claims_set

    def from_shared_secret_string(self, shared_secret_string, claims_set) -> None:
        super().__init__(shared_secret_string)
        self.claims_set = claims_set

    def verify(self, header, signing_input, signature) -> bool:
        value = super().verify(header, signing_input, signature)
        
        time = date.ctime()
        time = time * 1000
        
        not_before_time = self.claims_set.get_not_before_time().getTime() <= time
        before_expiration = time < self.claims_set.get_expiration_time().getTime()

        return value and not_before_time and before_expiration
