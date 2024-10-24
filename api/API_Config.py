import os
from dotenv import load_dotenv, find_dotenv, set_key
from dataclasses import dataclass
class password(str):
    def __str__(self):
        return '*' * len(self)
    
@dataclass(frozen=False)
class _API_Config:
    MPA_HOST:str|None = os.getenv('MPA_HOST') 
    MPA_UID:str|None = os.getenv('MPA_UID') 
    MPA_PW:password|None = password(os.getenv('MPA_PW'))
    MPA_CONTAINER:str|None = os.getenv("MPA_CONTAINER") 
    SNOW_HOST:str|None = os.getenv('SNOW_HOST') 
    SNOW_UID:str|None = os.getenv('SNOW_UID') 
    SNOW_PW:password|None = password(os.getenv('SNOW_PW'))
    def __init__(self):
        self.path = find_dotenv()
        load_dotenv(self.path)

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

