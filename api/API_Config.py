import os
from dotenv import load_dotenv, find_dotenv, set_key
from dataclasses import dataclass
class password(str):
    def __str__(self):
        return '*' * len(self)
    
@dataclass(frozen=False)
class _API_Config:
    _self = None
    MPA_HOST:str|None = os.getenv('MPA_HOST') 
    MPA_UID:str|None = os.getenv('MPA_UID') 
    MPA_PW:password|None = password(os.getenv('MPA_PW'))
    MPA_CONTAINER:str|None = os.getenv("MPA_CONTAINER") 
    SNOW_HOST:str|None = os.getenv('SNOW_HOST') 
    SNOW_UID:str|None = os.getenv('SNOW_UID') 
    SNOW_PW:password|None = password(os.getenv('SNOW_PW'))

    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self
    
    def _getEnvironment(self, key):
        val = os.getenv(key)   
        if (val==None):
            raise ValueError(f"{key} not set in .env file.  Run api/API_config.py.")
        return(val)
    
    def __init__(self):
        self.path = find_dotenv()
        load_dotenv(self.path)
        MPA_HOST =self._getEnvironment('MPA_HOST') 
        MPA_UID=self._getEnvironment('MPA_UID') 
        MPA_PW = password(self._getEnvironment('MPA_PW'))
        MPA_CONTAINER =self._getEnvironment("MPA_CONTAINER") 
        SNOW_HOST =self._getEnvironment('SNOW_HOST') 
        SNOW_UID =self._getEnvironment('SNOW_UID') 
        SNOW_PW = password(self._getEnvironment('SNOW_PW'))

    def save(self):
        for field in self.__dataclass_fields__:
            value = getattr(_API_Config, field)
            if not os.path.exists(self.path):
                print("creating .env file")
                self.path = ".env"
                open(self.path, "x")             
            set_key(self.path, key_to_set=field, value_to_set=value)
        
    def prompt(self):
        for field in _API_Config.__dataclass_fields__:
            while True:
                value = getattr(_API_Config, field)
                setattr(_API_Config, field, input(f"{field} ({value}):") or value)
                if (getattr(_API_Config, field)) :
                    break    
        
API_Config = _API_Config()

if __name__ == "__main__":
    API_Config.prompt()
    API_Config.save()

