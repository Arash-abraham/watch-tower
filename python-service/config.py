# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config(dict):
    def __init__(self):
        super().__init__()
        self.update({
            "DB_HOST": os.getenv("DB_HOST", "localhost"),
            "DB_USER": os.getenv("DB_USER", "root"),
            "DB_PASS": os.getenv("DB_PASS", ""),
            "DB_NAME": os.getenv("DB_NAME", "watch-tower"),
            "DB_PORT": os.getenv("DB_PORT", "3306"),
            "WATCH_DIR": os.getenv("WATCH_DIR"),
        })
    
    def __getattr__(self, key):
        return self.get(key)
    
    def __setattr__(self, key, value):
        self[key] = value

config = Config()
