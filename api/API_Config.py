import os
from dotenv import load_dotenv, find_dotenv, set_key
from dataclasses import dataclass

@dataclass(frozen=False)
class API_Config:
    MPA_HOST:str|None = os.getenv('MPA_HOST') 
    MPA_UID:str|None = os.getenv('MPA_UID') 
    MPA_PW:str|None = os.getenv('MPA_PW') 
    MPA_CONTAINER:str|None = os.getenv("MPA_CONTAINER") 
    SNOW_HOST:str|None = os.getenv('SNOW_HOST') 
    SNOW_UID:str|None = os.getenv('SNOW_UID') 
    SNOW_PW:str|None = os.getenv('SNOW_PW') 
    def __init__(self):
        self.path = find_dotenv()
        load_dotenv(self.path)

    def save(self):
        for key,value in self.__dict__.items():
            if (key=='path'): 
                continue
            set_key(self.path, key_to_set=key, value_to_set=value)
        print("Saved")

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(API_Config.__dict__)
