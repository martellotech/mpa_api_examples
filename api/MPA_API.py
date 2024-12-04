import http.client
from base64 import b64encode
import json
import logging
logger = logging.getLogger("MPA")
class MPA_API:
    class MPA_API_Exception(Exception):
        def __init__(self, message, errors=None):            
            super().__init__(message)
            self.errors = errors

    def userGuid(self):
        """Get User GUID
        Args:
            none.
        """
        if (not hasattr(self, 'me')):
            self.getMe()
        return(self.me['GUID'])
    
    def getMe(self):
        """Get User Object
        Args:
            none.
        """
        self.conn.request("GET", "/central/rest/me", "", self.headers)
        res = self.conn.getresponse()
        logger.debug(f"code: {res.getcode()}")
        if (res.getcode() == 302):
            logger.debug(f"redirect:{res.getheader('Location')}")
            res.read()
            self.conn.request("GET", res.getheader('Location'), "", self.headers)
            res = self.conn.getresponse()
        if (res.getcode() != 200):
            raise MPA_API.MPA_API_Exception("getMe Failure.", res.getcode())
        self.me = json.loads(res.read())
        return(self.me)
    
    def _basic_auth(self, username, password):
        token = b64encode(bytes(username, 'utf-8')+bytes(":", 'utf-8')+bytes(password,'utf-8'))
        return f'Basic {token.decode("utf-8")}'
    
    def __init__(self, host, uid, pw) -> None:
        """create a reusable REST API connector

        Args:
            host (host address): i.e. host.marwatch.net 
            uid (user id): email address of user
            pw (password): password mtching user
        """        
        self.host = host
        self.conn  = http.client.HTTPSConnection(host)
        self.headers = { 'Authorization': self._basic_auth(uid, pw) }  
    
if __name__ == "__main__":
    from .API_Config import API_Config
    import json
    mpa = MPA_API(API_Config.MPA_HOST, API_Config.MPA_UID, API_Config.MPA_PW)
    me = mpa.getMe()
    print(json.dumps(me))


