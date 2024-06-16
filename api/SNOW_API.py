import http.client
from base64 import b64encode
import json

class SNOW_API:

    def _basic_auth(self, username, password):
        token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f'Basic {token}'

    def createIncident(self, desc, comments=None):
        payload_object = {"short_description":desc}
        if (comments):
            payload_object['comments'] = comments
        payload = json.dumps(payload_object)
        self.conn.request("POST", "/api/now/table/incident", payload, self.headers )
        res = self.conn.getresponse()
        data = json.loads(res.read())
        data['Location'] = res.headers['location']
        return(data)

    def __init__(self, host, uid, pw) -> None:
        self.host = host
        self.conn  = http.client.HTTPSConnection(host)
        self.headers = { 'Authorization': self._basic_auth(uid, pw) }

if __name__ == "__main__":
    from api.API_Config import API_Config
    snow = SNOW_API(API_Config.SNOW_HOST, API_Config.SNOW_UID, API_Config.SNOW_PW)
    resp = snow.createIncident("TESTING SNOW API", "Comment [code]<a href=\"https://google.com\" target=\"_blank\">Google</a>[/code]")
    print(f"RESPONSE:{resp}")