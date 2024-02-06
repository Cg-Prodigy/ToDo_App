from datetime import datetime

from pydantic import BaseModel,Field
from tinydb import TinyDB,Query
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer


serializer=SerializationMiddleware(JSONStorage)
serializer.register_serializer(DateTimeSerializer(),"TinyDate")
db=TinyDB("app_data.json",storage=serializer)
qr=Query()

class UserData(BaseModel):
    username:str
    signup_day:datetime=datetime.today().now()

    def save(self):
        table=db.table("user_data")
        table.insert(
            {
                "username":self.username,
                "s_data":self.signup_day
            }
        )
        return True

class TaskData(BaseModel):
    title:str=Field(max_length=20)
    description:str|None=None
    completed:bool=False
    category:str
    start_time:datetime
    end_time:datetime
    month:str|None=None
    day:int|None=None
    def save(self):
        table=db.table("task_data")
        table.insert({
            "title":self.title,
            "description":self.description,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "completed":self.completed,
            "category":self.category,
            "month":self.start_time.date().strftime("%B"),
            "day":int(self.start_time.date().strftime("%d"))
        })
