import json
from api.MPA_API import MPA_API
import logging
logger = logging.getLogger("MPA")

class MPA_Alarms(MPA_API):
    def readAlarmList(self, container):
        """get MPA Alarms for container
        Args:
            container (GUID): container GUID
        """        
        self.conn.request("GET", f"/central/rest/containers/{container}/alarmList/", None, self.headers, encode_chunked=True)
        res = self.conn.getresponse()
        if (res.getcode()!=200):
            raise MPA_API.MPA_API_Exception("read alarm list failed", res.getcode())
        data = json.loads(res.read())
        return(data)
    
    def readAlarm(self, href):
        """get the details for an an alarm

        Args:
            href (MPA alarm href): inluded in each alarm returned by readAlarmList
        """        
        href = href.replace("https://"+self.host,"")
        self.conn.request("GET", href, "", self.headers)
        res = self.conn.getresponse()
        if (res.getcode()!=200):
            raise MPA_API.MPA_API_Exception("read alarm failed", res.getcode())
        data = json.loads(res.read())
        return(data)
    
    def updateTicket(self, href, number, url=None, ticket=None):
        """update a specific alarm with ticket number and URL

        Args:
            href (alarm ): returned by readAlarmList
            number (string): ticket number to display.  Can be any string.
            url (URL): link that will be added to string.
        """ 
        if (ticket):
            ticket['ticketinfo'] = {
                    "URL": url,
                    "number": number
            }
        else:
            ticket =   {
                "status": "New",
                "assignee": {
                    "name": "",
                    "GUID": ""
                },
                "ticketinfo": {
                    "URL": url,
                    "number": number
                }
            }     
        payload = json.dumps({"ticket":ticket})
        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self.headers)
        href = href.replace("https://"+self.host,"")
        href = href+f"/updateTicket/?user={self.me['GUID']}"
        self.conn.request("PUT", href, payload, headers)
        logger.debug(f"Updating Ticket: {href}")
        res = self.conn.getresponse()
        if (res.getcode()!=200):
            raise MPA_API.MPA_API_Exception("update ticket failed", res.getcode())
        data = json.loads(res.read())
        return(data)
