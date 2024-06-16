import unittest
import logging
import MPA_Alarms
from API_Config import API_Config

logger = logging.getLogger("mpa_alarms")

class Test_mpa_alarms(unittest.TestCase):  
    def setUp(self):
        self.mpa = MPA_Alarms.MPA_Alarms(API_Config.MPA_HOST, API_Config.MPA_UID, API_Config.MPA_PW)

    def test_get_userGuid_before_getMe(self):
        guid = self.mpa.userGuid()
        print(f"User: {guid}")
        self.assertTrue(guid is not None)

    def test_readAlarmList(self): 
        alarms =self.mpa.readAlarmList(API_Config.MPA_CONTAINER)
        self.assertTrue(bool(alarms), "No alarms retrieved")
        for a in alarms.keys():
            if ('ticketinfo' in alarms[a]['ticket'] ):
                logger.info(alarms[a]['ticket']['ticketinfo'])

    def test_updateTicket(self): 
        alarms =self.mpa.readAlarmList(API_Config.MPA_CONTAINER)
        self.mpa.userGuid()
        self.assertTrue(bool(alarms), "No alarms retrieved")
        a = next(iter(alarms))
        self.mpa.updateTicket(a, "TICKET", "https://ticket")
        alarm = self.mpa.readAlarm(a)
        self.assertTrue(alarm['ticket']['ticketinfo']['number']=="TICKET", "Ticket Number Set")
        self.assertTrue(alarm['ticket']['ticketinfo']['URL']=='https://ticket', "URL Set")
        self.mpa.updateTicket(a, "", "")
        alarm = self.mpa.readAlarm(a)
        self.assertTrue('ticketinfo' not in alarm['ticket'], "Ticket Number Cleared")

    def test_updateTicketWithNoURL(self): 
        alarms =self.mpa.readAlarmList(API_Config.MPA_CONTAINER)
        self.mpa.userGuid()
        self.assertTrue(bool(alarms), "No alarms retrieved")
        a = next(iter(alarms))
        self.mpa.updateTicket(a, "TICKET")
        alarm = self.mpa.readAlarm(a)
        self.assertTrue(alarm['ticket']['ticketinfo']['number']=="TICKET", "Ticket Number Set")
        self.assertTrue(alarm['ticket']['ticketinfo']['URL']=='null', "URL Not Set")
        self.mpa.updateTicket(a, "", "")
        alarm = self.mpa.readAlarm(a)
        self.assertTrue('ticketinfo' not in alarm['ticket'], "Ticket Number Cleared")
 

   