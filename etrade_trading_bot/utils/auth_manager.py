# Placeholder
import os 
import time 
import hmac 
import hashlib 
import base64 
import urllib.parse 
import uuid

class ETradeAuthManager: 
    """ Handles OAuth 1.0a header generation for E*TRADE API requests. Assumes you already have permanent access_token and token_secret. """
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def _get_oauth_params(self):
        """
        Constructs basic OAuth parameters.
        """
        return {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": uuid.uuid4().hex,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": str(int(time.time())),
            "oauth_token": self.access_token,
            "oauth_version": "1.0"
        }

    def _build_signature(self, method, url, oauth_params, additional_params={}):
        """
        Constructs OAuth signature for the request.
        """
        all_params = {**oauth_params, **additional_params}
        sorted_items = sorted(all_params.items())
        param_str = urllib.parse.urlencode(sorted_items, quote_via=urllib.parse.quote)

        base_string = "&".join([
            method.upper(),
            urllib.parse.quote(url, safe=""),
            urllib.parse.quote(param_str, safe="")
        ])

        signing_key = f"{urllib.parse.quote(self.consumer_secret)}&{urllib.parse.quote(self.access_token_secret)}"
        hashed = hmac.new(signing_key.encode(), base_string.encode(), hashlib.sha1)

        return base64.b64encode(hashed.digest()).decode()

    def generate_auth_header(self, method, url, additional_params={}):
        """
        Generates the full OAuth Authorization header.
        """
        oauth_params = self._get_oauth_params()
        signature = self._build_signature(method, url, oauth_params, additional_params)
        oauth_params["oauth_signature"] = signature

        header = "OAuth " + ", ".join([
            f'{urllib.parse.quote(k)}="{urllib.parse.quote(v)}"' for k, v in oauth_params.items()
        ])
        return {
            "Authorization": header
        }

if __name__ == "__main__":
    # Example usage — replace these with your real credentials CONSUMER_KEY = "YOUR_CONSUMER_KEY" CONSUMER_SECRET = "YOUR_CONSUMER_SECRET" ACCESS_TOKEN = "YOUR_ACCESS_TOKEN" ACCESS_TOKEN_SECRET = "YOUR_ACCESS_SECRET"
    auth_manager = ETradeAuthManager(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET
    )
    # Sample API call for quote endpoint
    test_url = "https://api.etrade.com/v1/market/quote/AAPL.json"
    headers = auth_manager.generate_auth_header("GET", test_url)
    print(headers)
    