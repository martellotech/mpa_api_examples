from api.MPA_Alarms import MPA_Alarms
from api.SNOW_API import SNOW_API
import time
import json
import logging
from api.API_Config import API_Config 
api_config = API_Config()
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
fh = logging.FileHandler('mpa_api.log')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

# Alarm attributes are:
# 'id', 'href', 'globalRating', 'userRating', 'groupRating', 
#'favorite', 'severity', 'text', 'source', 'starttime', 
# 'updatetime', 'hasExpireTime', 'hasEndTime', 'labels',
# 'requiresExplicitUserAcknowledgement', 'isAcknowledged', 
#'canBeAcknowledgedByUser', 'device', 'containers', 'ticket', 
# 'hidden', 'silenced'
#
# ticket has attributes 'status', 'assignee', 'ticketinfo'
#
# ticketinfo has attributes 'number', 'URL'

mpa = MPA_Alarms(api_config.MPA_HOST, api_config.MPA_UID, api_config.MPA_PW)
snow = SNOW_API(api_config.SNOW_HOST, api_config.SNOW_UID, api_config.SNOW_PW)
logging.info(f"MPA TO SNOW: {api_config.MPA_HOST} -> {api_config.SNOW_HOST}")
me = mpa.getMe()
logger.debug(json.dumps(me['GUID']))

def run_forever():
    try:
        while True:
            alarms = mpa.readAlarmList(api_config.MPA_CONTAINER)
            for a in alarms.keys():
                #logger.debug(alarms[a]['id'], alarms[a]['ticket'].keys())
                age = round(time.time() * 1000) - alarms[a]['starttime']
                if (((alarms[a]['severity'] == "CRITICAL")and(age < 60*60*1000)) or 
                    (alarms[a]['favorite']) or (alarms[a]['ticket']['status']=='Assigned')):
                    # if ticketinfo is blank, create a ticket in SNOW
                    if ('ticketinfo' not in alarms[a]['ticket'] ):
                        logger.info(f"new alarm:{alarms[a]['text']}{alarms[a]['ticket']}")
                        snow_text = f"{alarms[a]['device']['name']} - {alarms[a]['text']}"
                        dashboard = f"https://{api_config.MPA_HOST}/dashboard/container/?template=device/general&device={alarms[a]['device']['GUID']}"
                        snow_comment = f"Navigate to MPA Device [code]<a href=\"{dashboard}\" target=\"_blank\">{alarms[a]['device']['name']}</a>[/code]"
                        logger.debug(f"link to dashboard {dashboard}")
                        resp = snow.createIncident(snow_text, snow_comment)
                        snow_uri = f"https://{api_config.SNOW_HOST}/nav_to.do?uri=incident.do?sysparm_query=number={resp['result']['number']}"
                        logger.info(f"Created SNOW incident: {snow_text} {resp['result']['number']}")
                        mpa.updateTicket(a, resp['result']['number'], snow_uri)
                    else:
                        logger.debug(f"critical alarm with ticketinfo:{alarms[a]['text']}{alarms[a]['ticket']}")
            time.sleep(5)
    except Exception:
        logger.exception("Critical Failure, restarting")
        run_forever() # Careful.. recursive behavior
        # Recommended to do this instead
        handle_exception()

def handle_exception():
    # code here
    pass

run_forever()