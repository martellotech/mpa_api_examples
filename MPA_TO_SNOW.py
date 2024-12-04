from api.MPA_Alarms import MPA_Alarms
from api.SNOW_API import SNOW_API
import time
import json
import logging
from api.API_Config import API_Config 
from http import HTTPStatus
from requests.exceptions import HTTPError
import pandas as pd

logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S')
fh = logging.FileHandler('mpa_api.log')
#fh.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
logger = logging.getLogger("MPA")
# Switch to logger.setLevel(logging.DEBUG) to get more info.
logger.setLevel(logging.INFO)
logger.addHandler(fh)



# Don't abort if we get these errors:
retry_codes = [
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT
]

def run_forever():
    # Create API connectors
    mpa = MPA_Alarms(API_Config.MPA_HOST, API_Config.MPA_UID, API_Config.MPA_PW)
    snow = SNOW_API(API_Config.SNOW_HOST, API_Config.SNOW_UID, API_Config.SNOW_PW)
    logging.info(f"MPA TO SNOW: {API_Config.MPA_HOST} -> {API_Config.SNOW_HOST}")

    # Get MPA User Record
    me = mpa.getMe()
    logger.debug(f"MPA User record{json.dumps(me['GUID'])}")
    mpa_to_snow_mapping = pd.read_excel("./mpa_to_snow_mapping.xlsx")
    def raise_ticket(alarm, snow_text, snow_comment):
        logger.info(f"new alarm:{alarm['text']}{alarm['ticket']}")
        dashboard = f"https://{API_Config.MPA_HOST}/dashboard/container/?template=device/general&device={alarm['device']['GUID']}"
        logger.debug(f"link to dashboard {dashboard}")
        resp = snow.createIncident(snow_text, snow_comment)
        snow_uri = f"https://{API_Config.SNOW_HOST}/nav_to.do?uri=incident.do?sysparm_query=number={resp['result']['number']}"
        logger.info(f"Created SNOW incident: {snow_text} {resp['result']['number']}")
        mpa.updateTicket(a, resp['result']['number'], snow_uri, ticket=alarm['ticket'])
    
    try:
        while True:
            alarms = mpa.readAlarmList(API_Config.MPA_CONTAINER)
            logger.info(f"processing {len(alarms.keys())} alarms from container {API_Config.MPA_CONTAINER}")
            for a in alarms.keys():
                #logger.debug(alarms[a]['id'], alarms[a]['ticket'].keys())
                age = round(time.time() * 1000) - alarms[a]['starttime']
                '''
                Some example patterns for ticket automation:
                1. All new critical alarms 
                2. Any with the "favorite" (star) button checked (always ticket this kind of alarm)
                3. Any that have been assigned to a person.
                '''
                mapped = mpa_to_snow_mapping[mpa_to_snow_mapping['MPA Alarm Text']==alarms[a]['text']]
                if (mapped.size != 0):
                    if ('ticketinfo' not in alarms[a]['ticket'] ):
                        raise_ticket(alarms[a],mapped['SNOW Incident Title'][0], mapped['SNOW Incident Text'][0])
                elif (((alarms[a]['severity'] == "CRITICAL")and(age < 60*60*1000)) or 
                    (alarms[a]['favorite']) or 
                    (alarms[a]['ticket']['status']=='Assigned')):
                    # if ticketinfo is blank, create a ticket in SNOW
                    if ('ticketinfo' not in alarms[a]['ticket'] ):
                        snow_text = f"{alarms[a]['device']['name']} - {alarms[a]['text']}"
                        dashboard = f"https://{API_Config.MPA_HOST}/dashboard/container/?template=device/general&device={alarms[a]['device']['GUID']}"
                        snow_comment = f"Navigate to MPA Device [code]<a href=\"{dashboard}\" target=\"_blank\">{alarms[a]['device']['name']}</a>[/code]"
                        raise_ticket(alarms[a], snow_text, snow_comment)
                    else:
                        logger.debug(f"critical alarm with ticketinfo:{alarms[a]['text']} <-> {alarms[a]['ticket']['ticketinfo']['number']}")
            time.sleep(5)
            
    except HTTPError as e:
        code = e.response.status_code
        if (code in retry_codes):
            logger.warning(f"http error {code}. Continuing execution.") 
        logger.error("http error {code}. Exiting.")
        return #exit
    except Exception as e:
        logger.exception(e)
        logger.exception("Critical Failure, restarting")
    run_forever() 

def handle_exception():
    # code here
    pass

run_forever()