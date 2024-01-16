from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivy.metrics import dp

from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard

from datetime import datetime
from tinydb import TinyDB,Query
class EntryPoint(ScreenManager):
    def __init__(self,db ,**kwargs):
        super(EntryPoint,self).__init__(**kwargs)
        self.db=db
        self.add_widget(SignUpScreen(db))
        self.add_widget(HomeScreen(db))
        self.add_widget(CreateTask(db))
        self.transition.duration=.2
        if self.db.tables():
            self.current="homescreen"
        else:
            self.current="signup"
        

class SignUpScreen(MDScreen):
    usr_name=ObjectProperty()
    def __init__(self,db, *args, **kwargs):
        super(SignUpScreen,self).__init__(*args, **kwargs)
        self.db=db
        self.name="signup"
    def save_user_name(self):
        user_name=self.usr_name.text
        if not user_name:
            return
        user_table=self.manager.db.table("User Data")
        user_table.insert({"User Name":str(user_name)})
class HomeScreen(MDScreen):
    usr_name=ObjectProperty()
    user_time=ObjectProperty()
    def __init__(self,db:TinyDB, *args, **kwargs):
        super(HomeScreen,self).__init__(*args, **kwargs)
        self.name="homescreen"
        if db.tables():
            self.tables=db.table("User Data").all()
            self.usr_name.text=f"Welcome {self.tables[0]['User Name']}"
            Clock.schedule_interval(self.update_time,1)
    def update_time(self,*args):
        today=datetime.today().time()
        self.user_time.text=f"{today.strftime('%a: %H:%M:%S')}"

class CreateTask(MDScreen):
    def __init__(self,db:TinyDB, *args, **kwargs):
        super(CreateTask,self).__init__(*args, **kwargs)
        self.name="create_task"
        self.db=db
    def change_screen(self):
        self.manager.current="homescreen"
        self.manager.transition.direction="right"

    def create_group_task(self,txt_field):
        group_name=txt_field.text
        task_table=self.db.table("User Tasks")
        group_name=txt_field.text

