from api.MPA_Alarms import MPA_Alarms
from api.SNOW_API import SNOW_API
from config import Config
from api.API_Config import API_Config
import logging
import panel as pn
from panel.theme import Bootstrap
import pandas as pd
from datetime import datetime
import time
from bokeh.models.widgets.tables import  StringFormatter
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
snow = SNOW_API(api.SNOW_HOST, api.SNOW_UID, api.SNOW_PW)

#ALARM_COLORS = {"CRITICAL":"#f0b9b9", "MAJOR":"#F0d1bd", "MINOR":"#f0e8c2", "WARNING":"#c7edf0", "INDETERMINATE":"#ccdef0", "INFO":"#f7d2f7"}
def flatten(df):
    for c in df.columns:
        f = df[c].apply(pd.Series)
        if (f.shape[1]>1):
            if (0 in f.columns):
                f = f.drop(labels=0, axis=1)
            f.columns = [c+'.'+x for x in f.columns]
            f = flatten(f)
            df = pd.merge(df, f, right_index=True, left_index=True)
    return(df)
            
def alarms_to_table(alarms):
    keys_for_table = ['href', 'id', 'severity', 'text', 'starttime','device', 'ticket', 'source']
    a = []
    for v in iter(alarms):
        a.append([alarms[v][k] for k in keys_for_table])
    df= pd.DataFrame(a, columns=keys_for_table)
    df = flatten(df)
    df['time'] = pd.to_datetime(df['starttime'], unit='ms', origin='unix')
    df['ticket_number']=df['ticket'].apply(lambda t: None if 'ticketinfo' not in t else 
                                         (None if 'number' not in t['ticketinfo'] else t['ticketinfo']['number']))

    return(df)

table = alarms_to_table(mpa_alarms.readAlarmList(api.MPA_CONTAINER))
show = ['severity', 'text', 
        'device.name', 'device.type', 
        'ticket.status', 'ticket.assignee.name', 'ticket.ticketinfo.number'
       ]
hidden = [c for c in table.columns if c not in show]
tabulator = pn.widgets.Tabulator(table, hidden_columns=hidden, buttons={"Raise SNOW Ticket": "<i class='fa fa-pen-to-square'></i>"}, disabled=False,
                                show_index=False, width=1200)

frame = pn.widgets.DataFrame(table)
def raise_snow_incident(event):
    if (len(event)==0):
        return event
    alarm = tabulator.value.iloc[tabulator.selection[0]]
    snow_text = f"{alarm['device.name']} - {alarm['text']}"
    dashboard = f"https://{api.MPA_HOST}/dashboard/container/?template=device/general&device={alarm['device.GUID']}"
    snow_comment = f"Navigate to MPA Device [code]<a href=\"{dashboard}\" target=\"_blank\">{alarm['device.name']}</a>[/code]"
    resp = snow.createIncident(snow_text, snow_comment)
    snow_uri = f"https://{api.SNOW_HOST}/nav_to.do?uri=incident.do?sysparm_query=number={resp['result']['number']}"
    logger.info(f"Created SNOW incident: {snow_text} {resp['result']['number']}")
    mpa_alarms.updateTicket(alarm['href'], resp['result']['number'], snow_uri)
    return event

raise_snow_incident=pn.bind(raise_snow_incident, tabulator.param.selection)

alarmList = pn.Column(tabulator, raise_snow_incident, name="Alarms")
conf = Config()
tabs = pn.Tabs(frame, pn.Column(conf.view, conf.updateButton, name="Configuration"), alarmList)

def alarm_loop():
    table = alarms_to_table(mpa_alarms.readAlarmList())
    tabulator.value = table

pn.state.add_periodic_callback(alarm_loop, 15000)

tabs.show()


