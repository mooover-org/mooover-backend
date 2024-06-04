import json
from typing import Dict

from fastapi import HTTPException
from jose import jwt
from six.moves.urllib.request import urlopen
import time
import logging


class JwtValidator:
    """A JavaScript Web Token (JWT) validator"""

    def __init__(self, auth0_config: Dict[str, str]):
        self.auth0_config = auth0_config
        self.jwks_cache = None
        self.jwks_cache_expiry = 0
        self.logger = logging.getLogger(__name__)

    def _get_jwks(self) -> Dict:
        """Fetch JWKS (JSON Web Key Set) from Auth0, with caching."""
        current_time = time.time()
        if self.jwks_cache is None or current_time > self.jwks_cache_expiry:
            try:
                jsonurl = urlopen(f"{self.auth0_config['ISSUER']}.well-known/jwks.json")
                self.jwks_cache = json.loads(jsonurl.read())
                self.jwks_cache_expiry = current_time + 3600  # Cache for 1 hour
            except Exception as e:
                self.logger.error(f"Failed to fetch JWKS: {e}")
                raise HTTPException(status_code=500, detail="Failed to fetch JWKS")
        return self.jwks_cache

    def validate(self, token: str) -> None:
        """
        Validates a JavaScript Web Token.

        :param token: the token string value
        :return: None
        :raises HTTPException: if anything goes wrong during the validation process
        """
        try:
            jwks = self._get_jwks()
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks["keys"]:
                if key.get("kid") == unverified_header.get("kid"):
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
            else:
                raise HTTPException(status_code=401, detail="Unable to find appropriate key")
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token is expired")
            raise HTTPException(status_code=401, detail="Token is expired")
        except jwt.JWTClaimsError:
            self.logger.warning("Invalid claims, check audience and issuer")
            raise HTTPException(status_code=401, detail="Invalid claims, check audience and issuer")
        except jwt.JWTError:
            self.logger.warning("Token is invalid")
            raise HTTPException(status_code=401, detail="Token is invalid")
        except Exception as e:
            self.logger.error(f"An error occurred while validating the token: {e}")
            raise HTTPException(status_code=500, detail=f"An error occurred while validating the token: {e}")
