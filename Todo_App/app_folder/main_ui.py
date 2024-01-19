

from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.list import TwoLineIconListItem,IconLeftWidget



from tinydb import TinyDB,Query
qr=Query()
db=TinyDB("app_data.json")


class EntryPoint(MDScreenManager):
    def __init__(self,**kwargs):
        super(EntryPoint,self).__init__(**kwargs)
        self.transition.duration=.2
        if db.tables():
            self.current="homescreen"
        else:
            self.current="signup"

class SignUpScreen(MDScreen):
    user_name=ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(SignUpScreen,self).__init__(*args, **kwargs)
    def save_user_name(self):
        user_name=self.user_name.text
        if not user_name:
            return
        user_table=db.table("User Data")
        user_table.insert({"User Name":str(user_name)})
class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(HomeScreen,self).__init__(*args, **kwargs)
        self.grid_layout=MDGridLayout(
            cols=1,
            rows=2,
            padding=(5,5),
            spacing=2,
        )
        self.home_ui=HomeUI()
        self.user_name=self.home_ui.ids["user_name"]
        self.group_no=self.home_ui.ids["group_no"]
        self.task_no=self.home_ui.ids["task_no"]
        self.swiper=self.home_ui.ids["swiper"]
        self.grid_layout.add_widget(self.home_ui)
        self.add_widget(self.grid_layout)
        self.update_ui_data()
        self.create_group_containers()

    def update_ui_data(self):
        user_name=db.table("User Data").all()[0]["User Name"]
        user_task=db.table("User Tasks")
        group_no=user_task.all().__len__()
        task_no=sum([len(task["Task"]) for task in user_task.all()])
        self.group_no.text=str(group_no)
        self.task_no.text=str(task_no)
        self.user_name.text=str(user_name).title()
    def create_group_containers(self):
        task_data=db.table("User Tasks").all()
        for group in task_data:
            group_name=group["Group Name"]
            task_count=len(group["Task"])
            list_item=TwoLineIconListItem(
                text=f"Group: {group_name}",
                secondary_text=f"Task count: {task_count}",
                bg_color=get_color_from_hex("#002050"),
                radius=[7,7,7,7],
                theme_text_color="Custom",
                secondary_theme_text_color="Custom",
                text_color=get_color_from_hex("#F0F8FF"),
                secondary_text_color=get_color_from_hex("#FF4500"),
            )
            list_icon=IconLeftWidget(
                        icon="table-plus",
                        theme_icon_color="Custom",
                        icon_color=get_color_from_hex("#FF4500")
                                     )
            list_item.add_widget(list_icon)
            self.swiper.add_widget(list_item)

class CreateTask(MDScreen):
    group_btns=ObjectProperty()
    task_btns=ObjectProperty()
    def __init__(self, *args, **kwargs):
        super(CreateTask,self).__init__(*args, **kwargs)
        self.name="create_task"
        self.task_list=[]
        self.group_name=None
        self.task_count=5
        self.task_table=None
        self.query=None
        self.snackbar=Snackbar(
                radius=[7,7,7,7],
                snackbar_x=dp(10),
                snackbar_y=dp(5),
                size_hint_x=.9,
                pos_hint={"center_x":.5},
        )
        if len(self.task_list)>=1:
            self.add_create_button()
    def change_screen(self):
        self.manager.current="homescreen"
        self.manager.transition.direction="right"
    def check_group(self,text_field):
        task_table=db.table("User Tasks")
        self.query=task_table.search(qr["Group Name"] ==str(text_field.text).strip().title())

    def create_group_task(self,txt_field):
        group_name=txt_field.text
        self.task_table=db.table("User Tasks")
        group_name=txt_field.text
        if group_name:
            self.group_name=str(group_name).title()
            group_widget=TitleButton(str(group_name).title(),"folder-clock-outline","Group",self.task_list,self.task_btns)
            if len(self.group_btns.children)>=1:
                self.snackbar.text=f"Error! You have not added tasks to {group_name}."
                txt_field.text=""
                self.snackbar.open()
                return
            self.group_btns.add_widget(group_widget)
        else:
            self.snackbar.text="Group field cannot be empty."
            self.snackbar.open()
        pass
    def add_task(self,task_title):
        task_t:str=task_title.text
        if task_t in self.task_list:
            self.snackbar.text="Task with the same title already exists."
            self.snackbar.open()
            return
        if not task_t:
            self.snackbar.text="Title field cannot be empty."
            self.snackbar.open()
            return
        if not self.group_name:
            self.snackbar.text="Group field is empty."
            self.snackbar.open()
            return
        if len(self.task_list)>self.task_count:
            self.snackbar.text="Max count reached"
            self.snackbar.open()
            return
        self.task_list.append(task_t.title())
        if len(self.task_list)==1:
            task_title.text=""
            anchor_layout=MDAnchorLayout(
                anchor_x="right",
                anchor_y="bottom",
                id="btn_cont"
            )
            add_btn=MDFillRoundFlatIconButton(
                icon="table-plus",
                text="Create Group"
            )
            add_btn.on_release=self.add_group_task_to_db
            anchor_layout.add_widget(add_btn)
            self.group_btns.add_widget(anchor_layout)
        title_widget=TitleButton(task_t,"clock-check-outline","title",self.task_list,group_btns=self.group_btns)
        self.task_btns.add_widget(title_widget)
        task_title.text=""

    def add_group_task_to_db(self):
        doc={
            "Group Name":self.group_name,
            "Task":self.task_list
        }
        self.task_table.insert(doc)


# UI components
class HomeUI(MDCard):
    def __init__(self, *args, **kwargs):
        super(HomeUI,self).__init__(*args, **kwargs)
        self.size_hint_y=.3
        self.border_radius=50
        self.padding=0,5
        self.orientation="vertical"
        user_name=db.table("User Data").all()[0]
        self.ids["user_name"].text=user_name["User Name"]
        self.ids["group_no"].text=str(0)
        self.ids["task_no"].text=str(0)

class TitleButton(MDFillRoundFlatIconButton):
    def __init__(self,title,icon,id_, title_list:list,task_widget:ObjectProperty=None,group_btns:ObjectProperty=None,*args, **kwargs):
        super(TitleButton,self).__init__(*args, **kwargs)
        self.text=str(title).capitalize()
        self.icon=icon
        self.pos_hint={"top":1}
        self.title_list=title_list
        self.id=id_
        self.task_widget=task_widget
        self.group_btns=group_btns
    
    def on_release(self):
        if self.id=="Group":
            self.title_list=[]
            self.task_widget.clear_widgets()
            self.parent.clear_widgets()
            return
        self.title_list.remove(self.text)
        self.parent.remove_widget(self)
        if not self.title_list:
            create_widget=self.group_btns.children[0]
            self.group_btns.remove_widget(create_widget)