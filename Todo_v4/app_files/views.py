from datetime import datetime
from app_files.models import db,TaskData,UserData,qr

def collect_task_information():
   
    try:
        user_name=db.table("user_data").get(doc_id=1)["username"]
    except:
        user_name="Brian Ego"
    task_data=db.table("task_data").all()
    completed=len(list(filter(lambda x:x["completed"]==True,task_data)))
    total=len(task_data)
    complete_percent=0 if completed ==0 else (completed/total)*100
    data_dict={
        "total_percent":complete_percent,
        "username":user_name,
    }
    personal=dataInDict("category","Personal",task_data)
    work=dataInDict("category","Work",task_data)
    health=dataInDict("category","Health",task_data)
    social=dataInDict("category","Social",task_data)
    study=dataInDict("category","Study",task_data)
    data_dict["Personal"]=personal
    data_dict["Work"]=work
    data_dict["Health"]=health
    data_dict["Social"]=social
    data_dict["Study"]=study
    return data_dict

def save_task_data(data_dict:dict):
    instance=TaskData(
        title=data_dict["title"],
        description=data_dict["description"],
        category=data_dict["category"],
        start_time=data_dict["start_time"],
        end_time=data_dict["end_time"],
    )
    instance.save()

def save_user_data(user_name:str):
    user_name=user_name
    instance=UserData(
        username=user_name,
    )
    return instance.save()
def return_user():
    try:
        user=db.table("user_data").all()[0]
    except:
        user=None
    return user
def return_category_data(category:str):
    category_data=db.table("task_data").search(qr["category"]==category)
    return_data={}
    for data in category_data:
        data["doc_id"]=data.doc_id
        date:datetime=data["start_time"].date()
        month=date.strftime("%B")
        day=date.day
        if month in return_data.keys():
            if day in return_data[month].keys():
                return_data[month][day].append(data)
            else:
                return_data[month][day]=[]
                return_data[month][day].append(data)
        else:
            return_data[month]={}
            if day in return_data[month].keys():
                return_data[month][day].append(data)
            else:
                return_data[month][day]=[]
                return_data[month][day].append(data)
    return return_data


def delete_task(doc_id):
    return db.table("task_data").remove(doc_ids=[doc_id])
def completed_task(doc_id):
    return db.table("task_data").update({"completed":True},doc_ids=[doc_id])
        

def task_month_day(month,day):
    return db.table("task_data").search((qr["month"]==month)&(qr["day"]==day))


# utility functions 
def filter_data(key,val,data,more):
    that_do= list(filter(lambda x:x[key]==val,data))
    if more:
        that_dont= list(filter(lambda x:x[key]!=val,data))
        return that_do,that_dont
    return that_do

def dataInDict(category,key,data):
    data=filter_data(category,key,data,False)
    completed,pending=filter_data("completed",True,data,True)
    percentage= 0.5 if len(completed) == 0 else len(completed)/len(data)*360.5
    done_count=len(completed)
    left_count=len(pending)
    task_count=len(data)
    data_dict={
        f"{key}_done":completed,
        f"{key}_pending":pending,
        "total_count":task_count,
        "percentage":percentage,
        "done_count":done_count,
        "left_count":left_count,
        "category":key
    }
    return data_dict