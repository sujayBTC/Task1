from fastapi import FastAPI
from pydantic import BaseModel,Field
from uuid import UUID,uuid4
from typing import Optional

# database
import mysql.connector

app=FastAPI()

db=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='employee'
)

cursor=db.cursor()

userData=[
    {"id":"c89c0e84-f043-4c10-b0a2-1308525f562c","name":"sujay","email":"suj.com","department":"front"},
    {"id":"6ba896e4-969d-46f6-9abf-6aa64e7fdede","name":"sujay","email":"sujay.com","department":"front"},
    {"id":"bd43babe-8e59-45aa-ac9a-8c58d3996ec9","name":"sujay","email":"sujayselvan.com","department":"front"}
]

department = [
    {
        "id": 1,
        "name": "HR"
    },
    {
        "id": 2,
        "name": "Development"
    },
    {
        "id":3,
        "name":"Admin"
    }
]

# database operation

class userSchema(BaseModel):
    name:str
    email:str
    department:int

class updateShema(BaseModel):
    name:Optional[str] = None
    email:Optional[str] = None
    department:Optional[int] = None

# @app.post('/')
# def NewUser(data:userSchema):
#     mdata=data.dict()
#     if len(userData)!=0:      
#         for res in userData:
#             if res["email"] == mdata["email"]:
#                 return {"msg":"duplicate email", "email": mdata["email"]}

#         for res in department:
#             if res["id"] == mdata["department"]:
#                 mdata["department"]=res
#                 userData.append(mdata)  
#     else:
#         userData.append(mdata)
#         return {"msg":"successfully created","userID":mdata["id"]}
    
#     return {"msg":"successfully created","userID":mdata["id"]}

# @app.get('/{id}')
# def getData(id:UUID):
#     for res in userData:
#         # print(res["id"]==str(id))
#         if res["id"] == str(id):
#             return res
#         else:
#             # return {"msg":"please check your id"}
#             pass

# @app.put('/update/{id}')
# def userUpdate(id:UUID,data:updateShema):
#     # print(id)
#     modata=data.dict()
#     for res in userData:
#         print(type(res["id"]),type(str(id)))
#         if res["id"]==str(id):
#                 if modata["name"] != None:
#                     res["name"]=modata["name"]
#                     print("updated")
#                 if modata["email"] != None:
#                     res["email"]=modata["email"]
#                     print("updated")
#                 if modata["department"] != None:
#                     for dep in department:
#                         if dep["id"] == modata["department"]:
#                             res["department"]=dep
#                         print("updated")
        

# @app.delete('/delete/{delid}')
# def deleteUser(delid:UUID):
#     for res in userData:
#         if res["id"]==(delid):
#             userData.remove(res)

# @app.get('/')
# def showALl():
#     return userData


# curd with dataBase

@app.get('/')
def get_user():
    cursor.execute(f"select * from user")
    result=cursor.fetchall()
    return result

@app.get('/{id}')
def get_single_user(id:int):
    cursor.execute(f'select * from user where id={id}')
    res=cursor.fetchall()
    return res

@app.post('/')
def add_user(data:userSchema):
    # print(data)
    for x in department:
        # print(x["id"])
        if x["id"] == data.department:
            # print("working")
            data.department = x["name"] 
    cursor.execute(f"insert into user(name,email,dep) values ('{data.name}','{data.email}','{data.department}')")
    db.commit()
    return {"message":"user added"}

@app.put('/{id}')
def user_Update(id:int,data:updateShema):
    # print(data)
    if data.name != "string":
        cursor.execute(f"update user set name='{data.name}' where id={id}")
    if data.email !="string":
        cursor.execute(f"update user set email='{data.email}' where id={id}")
    if data.department !=0:
        for x in department:
          if x["id"] == data.department:
            data.department = x["name"] 
        cursor.execute(f"update user set dep='{data.department}' where id={id}")
    else:
        return {"message":"enter valid data"}
    
    # cursor.execute(f"update user set name='{data.name}',email='{data.email}',dep='{data.department}' where id={id}")
    db.commit()
    return {"message":"user updated"}

@app.delete('/{id}')
def remove_user(id):
    cursor.execute(f"delete from user where id={id}")
    db.commit()
    return {"message":"user deleted successfully"}