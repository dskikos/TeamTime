from peewee import *
from datetime import datetime, date
import os

# Get absolute path to database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'teamtime.db')

db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class Activity(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    app_name = CharField()
    window_title = CharField()
    category = CharField(null=True)
    duration_seconds = IntegerField(default=0)

    class Meta:
        table_name = 'activities'

class Goal(BaseModel):
    date = DateField(default=date.today)
    target_minutes = IntegerField()
    completed = BooleanField(default=False)

    class Meta:
        table_name = 'goals'

class Progress(BaseModel):
    date = DateField(default=date.today, unique=True)
    productive_minutes = FloatField(default=0)
    distracting_minutes = FloatField(default=0)
    neutral_minutes = FloatField(default=0)

    class Meta:
        table_name = 'progress'

class XPRecord(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    xp_change = IntegerField()
    total_xp = IntegerField()
    reason = CharField()

    class Meta:
        table_name = 'xp_records'

class BlockRecord(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    action = CharField()  # activate, deactivate, emergency_unlock
    reason = CharField()
    blocked_sites = TextField()

    class Meta:
        table_name = 'block_records'

def initialize_database():
    db.connect()
    db.create_tables([Activity, Goal, Progress, XPRecord, BlockRecord])
    db.close()
