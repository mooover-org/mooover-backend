import json

from fastapi import HTTPException
from jose import jwt
from six.moves.urllib.request import urlopen


class JwtValidator:
    """A javascript web token validator"""

    def __init__(self, auth0_config: dict):
        self.auth0_config = auth0_config

    def validate(self, token: str) -> None:
        """
        Validates a javascript web token.

        :param token: the token string value
        :return: None
        :raises HTTPException: if anything goes wrong during the validation process
        """
        try:
            jsonurl = urlopen(
                f"{self.auth0_config['ISSUER']}.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            if rsa_key:
                jwt.decode(
                    token,
                    rsa_key,
                    algorithms=[self.auth0_config["ALGORITHM"]],
                    audience=self.auth0_config["AUDIENCE"],
                    issuer=self.auth0_config["ISSUER"],
                )
        except jwt.ExpiredSignatureError as e:
            raise HTTPException(status_code=401, detail="Token is expired")
        except jwt.JWTClaimsError as e:
            raise HTTPException(status_code=401, detail="Invalid claims, check "
                                                        "audience and issuer")
        except jwt.JWTError as e:
            raise HTTPException(status_code=401, detail="Token is invalid")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Unable to parse "
                                                        "authentication token")
