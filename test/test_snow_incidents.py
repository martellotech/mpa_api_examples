import unittest
import logging
from api.SNOW_API import SNOW_API
from api.API_Config import API_Config
logger = logging.getLogger("mpa_alarms")

class Test_SNOW_incidents(unittest.TestCase):  
    def setUp(self):
        self.snow = SNOW_API(API_Config.SNOW_HOST, API_Config.SNOW_UID, API_Config.SNOW_PW)

    def test_create_incident_with_comment(self): 
        resp = self.snow.createIncident("TESTING SNOW API", "Comment [code]<a href=\"https://google.com\" target=\"_blank\">Google</a>[/code]")
        print(f"RESPONSE:{resp}")
        self.assertTrue(str(resp['result']['number']).startswith("INC"))

    def test_create_incident_without_comment(self): 
        resp = self.snow.createIncident("TESTING SNOW API")
        print(f"RESPONSE:{resp}")
        self.assertTrue(str(resp['result']['number']).startswith("INC"))

   