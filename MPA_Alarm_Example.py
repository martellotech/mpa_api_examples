from api.MPA_Alarms import MPA_Alarms
from config import Config
from api.API_Config import API_Config
import logging
import panel as pn
from panel.theme import Bootstrap
import pandas as pd
from datetime import datetime
import time
api = API_Config()
pn.extension('terminal', console_output='disable')
logger = logging.getLogger('mpa_api')
logger.setLevel(logging.DEBUG)
debug = pn.widgets.Debugger(logger_names=["mpa_api"], level=logging.DEBUG, design=Bootstrap)
logger.info("Starting...")

pn.extension("tabulator", css_files=["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"])

mpa_alarms = MPA_Alarms(api.MPA_HOST, api.MPA_UID, api.MPA_PW)
me = mpa_alarms.getMe()
logger.info(f"MPA User:{me}")

def alarms_to_table(alarms):
    keys_for_table = ['id', 'severity', 'text', 'starttime', 'device', 'ticket', 'source']
    a = []
    for v in iter(alarms):
        a.append([alarms[v][k] for k in keys_for_table])
    df= pd.DataFrame(a, columns=keys_for_table)
    df['time'] = pd.to_datetime(df['starttime'], unit='ms', origin='unix')
    df['ticket_number']=df['ticket'].apply(lambda t: None if 'ticketinfo' not in t else 
                                         (None if 'number' not in t['ticketinfo'] else t['ticketinfo']['number']))
    return(df)

table = alarms_to_table(mpa_alarms.readAlarmList(api.MPA_CONTAINER))

tabulator = pn.widgets.Tabulator(table, buttons={"Trash": "<i class='fa fa-trash'></i>"}, disabled=True)
def update_selection(event):
    tabulator.value=tabulator.value.iloc[list(set(tabulator.value.index)-set(tabulator.selection))]
    return event

update_selection=pn.bind(update_selection, tabulator.param.selection)

alarmList = pn.Column(tabulator, update_selection, name="Alarms")
conf = Config()
tabs = pn.Tabs(pn.Column(conf.view, conf.updateButton, name="Configuration"), alarmList)
tabs.show()

def alarm_loop():
    table = alarms_to_table(mpa_alarms.readAlarmList())
    tabulator.value = table
    time.sleep(15)

