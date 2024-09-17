import os
from dotenv import load_dotenv, find_dotenv, set_key
from dataclasses import dataclass
class password(str):
    def __str__(self):
        return '*' * len(self)
    
@dataclass(frozen=False)
class API_Config():
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
        for field in API_Config.__dataclass_fields__:
            value = getattr(API_Config, field)
            set_key(self.path, key_to_set=field, value_to_set=value)
        print(f"Saved to {self.path}")
        
    def prompt(self):
        for field in API_Config.__dataclass_fields__:
            while True:
                value = getattr(API_Config, field)
                setattr(API_Config, field, input(f"{field} ({value}):") or value)
                if (getattr(API_Config, field)) :
                    break    
        
            

if __name__ == "__main__":
    a = API_Config()
    a.prompt()
    a.save()

