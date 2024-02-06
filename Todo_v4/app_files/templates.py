
from pprint import pprint
from datetime import datetime,timedelta

from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager,FadeTransition
from kivy.utils import get_color_from_hex
from kivy.graphics import Color,Line
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.uix.widget import MDWidget
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDTimePicker,MDDatePicker
from kivymd.uix.dialog import MDDialog



from app_files.views import collect_task_information,save_task_data,save_user_data,return_user,return_category_data,\
delete_task,completed_task,task_month_day

TIME_NOW=datetime.now().time()

bg_colors={
    "bg_one":get_color_from_hex("#27374D"),
    "bg_two":get_color_from_hex("#DDE6ED"),
    "bg_three":get_color_from_hex("#526D82"),
    "bg_four":get_color_from_hex("#9DB2BF"),
    "bg_five":get_color_from_hex("#FFFFFF")
}
text_colors={
    "txt_one":get_color_from_hex("#1597BB"),
    "txt_two":get_color_from_hex("#FF4C29"),
    "txt_three":get_color_from_hex("#EEEEEE"),
    "txt_four":get_color_from_hex("#46C2CB")
}
class EntryPoint(ScreenManager):
    def __init__(self, **kwargs):
        super(EntryPoint,self).__init__(**kwargs)
        self.transition=FadeTransition()
        self.transition.duration=.3
        self.home_screen=HomeScreen(name="homescreen")
        self.create_task=CreateTask(name="createtask")
        self.sign_up=SignUpScreen(name="signup")
        self.task_screen=TaskDetails(name="taskscreen",category="Personal")
        if return_user():
            self.switch_to(self.home_screen)
            return
        self.switch_to(self.sign_up)
    def change_screen(self,from_screen,to_screen,category=None):
        if from_screen =="homescreen" and to_screen=="createtask":
            self.switch_to(self.create_task)
        if from_screen =="createtask" and to_screen=="homescreen":
            self.home_screen.create_ui()
            self.switch_to(self.home_screen)
        if from_screen=="signup" and to_screen=="homescreen":
            self.home_screen.create_ui()
            self.switch_to(self.home_screen)
        if from_screen=="taskscreen" and to_screen=="homescreen":
            self.home_screen.create_ui()
            self.switch_to(self.home_screen)
        if from_screen=="homescreen" and to_screen=="taskscreen":
            self.task_screen.category=category
            self.task_screen.load_ui_data()
            self.switch_to(self.task_screen)

class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_info=collect_task_information()
        self.progress:MDWidget=self.ids["progress"]
        self.progress_text=self.ids["progress_text"]
        self.user_name:MDWidget=self.ids["user_name"]
        self.task_category:MDWidget=self.ids["task_category"]
        self.task_categories=["Personal","Work","Study","Social","Health"]
        self.create_ui()
    def create_ui(self):
        Clock.schedule_once(self.create_canvas,.3)
        self.task_info=collect_task_information()
        self.percent= 0 if self.task_info["total_percent"] == 0 else (self.task_info["total_percent"]/100)*Window.width-dp(12)
        self.user_name.text=f"Welcome, [b]{self.task_info['username']}"
        self.progress_text.text=f"[b]{self.task_info['total_percent']:.0f}% of tasks are completed."
        if self.task_category.children:
            for each in self.task_category.children:
                category=each.task_data["category"]
                each.task_data=self.task_info[category]
                each.load_data()
        else:
            for each in self.task_categories:
                category=self.task_info[each]["category"]
                widget=CustomListItem(self.task_info[each])
                widget.load_data()
                widget.change_screen_btn.on_release=lambda x=category:self.manager.change_screen("homescreen","taskscreen",x)
                self.task_category.add_widget(widget)
    def create_canvas(self,*args):
        with self.progress.canvas.after:
            Color(
                rgb=bg_colors["bg_two"]
            )
            Line(
                points=(self.progress.x+5,self.progress.y+dp(20),Window.width-dp(12),self.progress.y+dp(20)),
                width=dp(4)
            )
            Color(
                rgb=bg_colors["bg_one"]
            )
            if self.percent>0:
                Line(
                    points=(self.progress.x+5,self.progress.y+dp(20),self.percent,self.progress.y+dp(20)),
                    width=dp(3)
                )




class CreateTask(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_title=self.ids["task_title"]
        self.task_description=self.ids["task_description"]
        self.start_time_btn=self.ids["start_time_btn"]
        self.start_time=self.ids["start_time"]
        self.end_time_label=self.ids["end_time_label"]
        self.task_category=self.ids["task_category"]
        self.start_date_btn=self.ids["start_date_btn"]
        self.start_date=self.ids["start_date"]
        self.today_checkbox=self.ids["today_checkbox"]
        self.end_time_btn=self.ids["end_time_btn"]
        self.start_date_val=None
        self.end_date_val=None
        self.task_data={
            "title":None,
            "description":None,
            "start_time":None,
            "end_time":None,
            "category":"Personal",
        }
        menu_items=[
            {
                "text":f"{i}",
                "viewclass":"OneLineListItem",
                "text_color":bg_colors["bg_one"],
                "theme_text_color":"Custom",
                "on_release":lambda x=f"{i}":self.set_category(x),
            } for i in ["Personal","Work","Study","Health","Social"]
        ]
        self.dropdown_menu=MDDropdownMenu(
            max_height=dp(230),
            width_mult=3,
            ver_growth="up",
            height=dp(20),
            items=menu_items,
            caller=self.task_category,
            background_color=bg_colors["bg_two"]
        )
        self.start_time_picker=MDTimePicker(
            primary_color=bg_colors["bg_four"],
            text_color=text_colors["txt_one"],
            accent_color=bg_colors["bg_two"],
            text_button_color=bg_colors["bg_one"],
        )
        self.end_time_picker=MDTimePicker(
            primary_color=bg_colors["bg_four"],
            text_color=text_colors["txt_one"],
            accent_color=bg_colors["bg_two"],
            text_button_color=bg_colors["bg_one"],
        )
        self.date_picker=MDDatePicker(
            min_year=datetime.today().year,
            max_year=datetime.today().year,
            min_date=datetime.today().date()+timedelta(days=2),
            title_input="Start Date",
            title="Start Date",
            primary_color=bg_colors["bg_one"],
            selector_color=text_colors["txt_two"]
        )
        self.date_picker.bind(on_save=self.get_select_date)


        self.start_time_picker.set_time(TIME_NOW)
        self.start_time_picker.bind(on_save=self.get_select_time)

        self.end_time_picker.bind(on_save=self.get_end_time)
        # dialog
        self.dialog=MDDialog(
            title="Error",
            buttons=[
                CustomBtn(
                    text="Cancel",
                    on_release=lambda x:self.dialog.dismiss()
                )
            ]
        )
    def open_datetime_dialog(self):
        if self.today_checkbox.active==True:
            self.today_checkbox.active=False
            self.start_date.text="Start Date:"
        self.date_picker.open()
    
    def get_select_date(self,*args):
        today=datetime.today().date()
        if args[1]<today:
            self.start_date.text="Error! Selected date is behind the current date."
            return
        self.start_date_val=args[1]
        self.start_date.text=f"[b]Selected Date: {args[1].strftime('%Y-%m-%d')}"
    
    def set_date_today(self,checkbox,value):
        if checkbox.state=="down":
            today=datetime.today().date()
            self.start_date.text=f"[b]Selected Date: {today.strftime('%Y-%m-%d')}"
            self.start_date_val=today
        else:
            self.start_date.text="End date:"
            self.start_date_val=None
    # title
    def validate_input(self,instance):
        if not instance.focus:
            if instance==self.task_title:
                title=instance.text
                if not title:
                    self.task_title.helper_text="Value cannot be empty"
                    self.task_title.error=True
                    return
                else:
                    self.task_data["title"]=str(title).strip().title()
                    return
            elif instance==self.task_description:
                desc=instance.text
                if not desc:
                    self.task_data["description"]=None
                    return
                self.task_data["description"]=str(desc).strip()
                return
        else:
            instance.helper_text=""
    # start_time
    def open_time_dialog(self):
        self.start_time_picker.open()
    def get_select_time(self,instance,time):
        if self.start_date_val:
            time_now=datetime.combine(datetime.today(),time=TIME_NOW)
            select_time=datetime.combine(date=self.start_date_val,time=time)
            time_diff=select_time-time_now
            if time_diff.days<0:
                self.start_time.text="Error! Selected time is behind the current time."
                self.task_data["start_time"]=""
            else:
                self.start_time.text=f'[b]Start Time: {select_time.strftime("%a %d - %H:%M %p")}[/b]'
                self.task_data["start_time"]=select_time
            
        else:
            self.start_time.text="Error! You need a start date."
        
        instance.dismiss()
    # end time
    def open_end_time(self):
        self.end_time_picker.open()
    
    def get_end_time(self,instance,time):
        if self.task_data["start_time"]:
            end_time=datetime.combine(self.task_data["start_time"],time=time)
            if end_time<self.task_data["start_time"]:
                self.end_time_label.text="Error! End time cannot be behind start time."
                self.task_data["end_time"]=None
            elif end_time==self.task_data["start_time"]:
                self.end_time_label.text="Error! End time cannot be equal to start time."
                self.task_data["end_time"]=None
            else:
                duration=end_time-self.task_data["start_time"]
                self.task_data["end_time"]=end_time
                self.end_time_label.text=f'[b]End Time: {end_time.strftime("%a %d - %H:%M %p")}'
        else:
            self.end_time_label.text="Error! You need a start time."
            
    # category
    def open_category_dropdown(self):
        self.dropdown_menu.open()
    def set_category(self,value):
        self.task_category.text=value
        self.task_data["category"]=value
        self.dropdown_menu.dismiss()
    
    # validate data
    def validate_data(self):
        message=None
        if not self.task_data["title"]:
            message="Please review the Title field."
        elif not self.task_data["start_time"]:
            message="Please review the Start Time field"
        elif not self.task_data["end_time"]:
            message="Please review the End Time field"
        
        if message:
            self.dialog.text=message
            self.dialog.open()
            return
        save_task_data(self.task_data)
        self.reset_layout()
        self.manager.change_screen("createtask","homescreen")
    def reset_layout(self):
        self.task_title.text=""
        self.task_description.text=""
        self.start_time.text=""
        self.end_time_label.text="End Time:"
        self.start_time.text="Start Time:"
        self.start_date.text="Start Date:"
        self.task_category.text="Personal"
        self.today_checkbox.active=False
        self.task_data={
            "title":None,
            "description":None,
            "start_time":None,
            "end_time":None,
            "category":"Personal"
        }

class SignUpScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super(SignUpScreen,self).__init__(*args, **kwargs)
        self.user_name=self.ids["user_name"]
        self.save_btn=self.ids["save_btn"]
        self.username=None
    def validate_data(self):
        if not self.user_name.focus:
            if not self.user_name.text.strip():
                self.user_name.helper_text="You need a user name to continue."
                self.save_btn.disabled=True
                return
            self.save_btn.disabled=False
            self.username=str(self.user_name.text).strip()
            self.user_name.helper_text=""
    def save_user(self):
        save_user_data(self.username)
        self.manager.change_screen("signup","homescreen")


class TaskDetails(MDScreen):
    def __init__(self,category,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category=category
        self.category_data=return_category_data(self.category)
        self.calendar_month=self.ids["calendar_month"]
        self.day_btns:MDWidget=self.ids["day_btns"]
        self.task_info:MDWidget=self.ids["task_info"]
        self.load_ui_data()
    def load_ui_data(self,month=None):
        self.category_data=return_category_data(self.category)
        date_time=datetime.today()
        months=list(self.category_data.keys())
        if month:
            if month not in months:
                return
            if month ==self.month:
                return
            self.month=month
            
        elif months:
            self.month=date_time.month if date_time.month in months else months[0]
        self.day_btns.clear_widgets()
        self.task_info.clear_widgets()
        if list(return_category_data(self.category).keys()):
            days=list(self.category_data[self.month].keys())
            if days:
                active_btn=self.load_days(self.month)
                day=datetime.today().day if datetime.today().day in days else days[0]
                self.load_days_tasks(self.month,day,active_btn)

            menu_items=[
                {
                    "text":f"{i}",
                    "viewclass":"OneLineListItem",
                    "theme_text_color":"Custom",
                    "text_color":bg_colors["bg_one"],
                    "on_release":lambda x= f"{i}":self.set_month(x),
                } for i in list(self.category_data.keys())
            ]
            self.month_dropdown=MDDropdownMenu(
                width_mult=3,
                ver_growth="up",
                max_height=dp(46)*len(list(self.category_data.keys())),
                caller=self.calendar_month,
                background_color=bg_colors["bg_two"],
                items=menu_items
            )
            self.calendar_month.text=self.month
        else:
            self.calendar_month.text="No Data"
    
    def open_dropdown(self):
        if self.calendar_month.text!="No Data":
            self.month_dropdown.open()

    # load days
    def load_days(self,month):
        days=sorted(list(return_category_data(self.category)[month].keys()))
        today=datetime.today().day if datetime.today().day in days else days[0]
        active_btn=None
        for day in days:
            btn=CustomBtn(
                icon="calendar-badge",
                text=str(day)
            )
            if day==today or days.index(day)==0:
                btn.md_bg_color=bg_colors["bg_one"]
                btn.text_color=text_colors["txt_two"]
                btn.icon_color=text_colors["txt_two"]
                btn.active_btn=True
                active_btn =btn
            btn.on_release=lambda x=btn:self.day_data(x)
            self.day_btns.add_widget(btn)
        return active_btn
    def load_days_tasks(self,month,day,btn):
        tasks=return_category_data(self.category)[month][int(day)]
        for task in tasks:
            task_dict={
                "title":f'[s][b]{task["title"]}[/b][/s]' if task["completed"]==True else f'[b]{task["title"]}[/b]',
                "description":task["description"],
                "doc_id":task.doc_id,
                "duration":f'{task["start_time"].strftime("%A %H:%M %p")} - {task["end_time"].strftime("%A %H:%M %p")}'
            }
            task_info=TaskCard(
                task_dict=task_dict,
                btn=btn
            )
            task_info.delete.on_release=lambda x=task_info,y=task,z=btn:self.delete_task(x,y,z)
            if task["completed"]==True:
                task_info.completed.disabled=True
            else:
                task_info.completed.on_release=lambda x=task_info,y=task.doc_id:self.set_complete(x,y)
            self.task_info.add_widget(task_info)
    def set_month(self,x):
        self.month_dropdown.dismiss()
        self.load_ui_data(month=x)
    
    def day_data(self,btn):
        if btn.active_btn==True:
            return
        else:
            for child in self.day_btns.children:
                if btn==child:
                    btn.active_btn=True
                    btn.md_bg_color=bg_colors["bg_one"]
                    btn.text_color=text_colors["txt_two"]
                    btn.icon_color=text_colors["txt_two"]
                else:
                    child.active_btn=False
                    child.md_bg_color=bg_colors["bg_five"]
                    child.text_color=bg_colors["bg_one"]
                    child.icon_color=bg_colors["bg_one"]
        self.task_info.clear_widgets()
        self.load_days_tasks(self.calendar_month.text,int(btn.text),btn)
    
    def delete_task(self,task_card,task,btn):
        child_count=len(task_card.parent.children)
        if child_count==1:
            index=list(self.day_btns.children).index(btn)
            if len(self.day_btns.children)>1:
                    day_btn=self.day_btns.children[index-1]
                    day_btn.active_btn=True
                    day_btn.md_bg_color=bg_colors["bg_one"]
                    day_btn.text_color=text_colors["txt_two"]
                    day_btn.icon_color=text_colors["txt_two"]
                    self.load_days_tasks(self.calendar_month.text,int(day_btn.text),day_btn)
            self.day_btns.remove_widget(btn)

        delete_task(task["doc_id"])
        self.task_info.remove_widget(task_card)

    def set_complete(self,task_info,doc_id):
        task_info.completed.disabled=True
        task_info.title.text=f'[s]{task_info.title.text}[/s]'
        completed_task(doc_id)
           











# components
class CustomListItem(MDCard):
    def __init__(self, task_data,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_data=task_data
        self.task_progress_cont:MDWidget=self.ids["task_progress_cont"]
        self.task_progress:MDWidget=self.ids["task_progress"]
        self.task_info:MDWidget=self.ids["task_info"]
        self.task_details:MDWidget=self.ids["task_details"]
        self.task_category=self.ids["task_category"]
        self.task_count=self.ids["task_count"]
        self.completed=self.ids["completed"]
        self.left=self.ids["left"]
        self.change_screen_btn=self.ids["change_screen_btn"]
        self.md_bg_color=bg_colors["bg_five"]
        self.size_hint_y:None
        self.load_data()
        
    def load_data(self):
        self.task_category.text=f"[b]{self.task_data['category']}[/b]"
        self.task_count.text=f"[b]No of tasks: {self.task_data['total_count']}"
        self.completed.text=f"{self.task_data['done_count']} completed"
        self.left.text=f"{self.task_data['left_count']} left"
        self.task_progress.text=f"{(self.task_data['percentage']/360.5)*100:.0f}%"
        with self.task_progress_cont.canvas:
            Color(
                rgb=bg_colors["bg_two"]
            )

            Line(
                circle=(
                    Window.width-dp(37),
                    self.task_progress.y+dp(5),
                    dp(10)),
                width=dp(2)
            )
            Color(
                rgb=text_colors["txt_two"]
            )
            Line(
                circle=(
                    Window.width-dp(37),
                    self.task_progress.y+dp(5),
                    dp(10),
                    0,
                    self.task_data["percentage"]
                    ),
                width=dp(2),
            )



class CustomTextField(MDTextField):
    def __init__(self, *args, **kwargs):
        super(CustomTextField,self).__init__(*args, **kwargs)
    
    def field_logic(self,hint_text):
        if self.focus:
            self.hint_text=hint_text
        else:
            self.hint_text=""

class CustomBtn(MDFillRoundFlatIconButton):
    def __init__(self, *args, **kwargs):
        super(CustomBtn,self).__init__(*args, **kwargs)
        self.active_btn=False

class TaskCard(MDCard):
    def __init__(self, task_dict,btn,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_dict=task_dict
        self.btn=btn
        self.doc_id=self.task_dict["doc_id"]
        self.title=self.ids["task_title"]
        self.description=self.ids["description"]
        self.duration=self.ids["duration"]
        self.completed=self.ids["completed"]
        self.delete=self.ids["delete"]
        self.title.text=f'[b]{self.task_dict["title"]}'
        self.description.text="No description" if not self.task_dict["description"] else self.task_dict["description"]
        self.duration.text=f'[i][b]{self.task_dict["duration"]}'
    
    # def delete_task(self):
    #     if len(self.parent.children)==1:
    #         self.btn.parent.remove_widget(self.btn)
    #     self.parent.remove_widget(self)
    #     delete_task(self.doc_id)
    
    def completed(self):
        pass