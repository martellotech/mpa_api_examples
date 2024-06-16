import panel as pn # ignore stub
from API_Config import API_Config

class Config(pn.Column):
    def __init__(self, **params):
        self.api = API_Config()
        super(Config, self).__init__(**params)  

    def view(self):
        self.mpa = pn.Column(pn.widgets.TextInput(name="MPA Host", value=self.api.MPA_HOST),
                         pn.widgets.TextInput(name="MPA Container", value=self.api.MPA_CONTAINER),
                         pn.widgets.TextInput(name="MPA User", value=self.api.MPA_UID),
                         pn.widgets.PasswordInput(name="MPA Password", value=self.api.MPA_PW)
                         )
        self.snow = pn.Column(pn.widgets.TextInput(name="Service Now Host", value=self.api.SNOW_HOST),
                         pn.widgets.TextInput(name="Service Now User", value=self.api.SNOW_UID),
                         pn.widgets.PasswordInput(name="Service Now Password", value=self.api.SNOW_PW)
                         )
        view = pn.Row(self.mpa, self.snow)             
        return(view)
    
    def update(self):
        self.api.SNOW_HOST = self.snow.objects[0].value
        self.api.SNOW_UID = self.snow.objects[1].value
        self.api.SNOW_PW = self.snow.objects[2].value
        self.api.MPA_HOST = self.mpa.objects[0].value
        self.api.MPA_CONTAINER = self.mpa.objects[1].value
        self.api.MPA_UID = self.mpa.objects[2].value
        self.api.MPA_PW = self.mpa.objects[3].value
        self.api.save()
        print("OK")

    def updateButton(self):
        updateConfig = pn.widgets.Button(name='Save Configuration', button_type='primary')
        updateConfig.on_click(lambda e:self.update())
        return(updateConfig)

