import os
from pathlib import Path

class Config:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / 'data'
    CONFIG_DIR = BASE_DIR / 'config'

    DATABASE_PATH = DATA_DIR / 'teamtime.db'
    CATEGORIES_PATH = CONFIG_DIR / 'categories.json'

    TRACKING_INTERVAL = 2
    PENALTY_FACTOR = 0.5

    DEFAULT_GOAL_MINUTES = 240

    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.DATA_DIR, exist_ok=True)
        os.makedirs(cls.CONFIG_DIR, exist_ok=True)
