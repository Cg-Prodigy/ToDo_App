from kivy.properties import ObjectProperty

from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager

from datetime import datetime
from tinydb import TinyDB,Query
class EntryPoint(ScreenManager):
    def __init__(self,db ,**kwargs):
        super(EntryPoint,self).__init__(**kwargs)
        self.db=db
        self.add_widget(SignUpScreen(db))
        self.add_widget(HomeScreen(db))
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
    def __init__(self,db:TinyDB, *args, **kwargs):
        super(HomeScreen,self).__init__(*args, **kwargs)
        self.name="homescreen"
        if db.tables():
            self.tables=db.table("User Data").all()
            self.usr_name.text=self.tables[0]["User Name"]