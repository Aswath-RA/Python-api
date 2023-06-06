from typing import Union
from typing import Optional
from fastapi import FastAPI ,Response,status,HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import random
import time

app = FastAPI()

class userPost(BaseModel):
    name : str
    age : int
    

#used to check the db if not connected api wont work,unless a sucessfull connection.
while (True):
   try :
     #connecting to database
     conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='password123',cursor_factory=RealDictCursor)
     cursor = conn.cursor()
     print("database connection sucessfull")
     break
   except Exception as error :
    print("Error: ,",error)
    time.sleep(2)


usersLocalArray = [{"name":"Aswath","age" : 23,"role":"ios Developer","companyname":"Vrdella","salary":"20k","empid":1},{"name":"John","age" : 30,"role":"Hitman","companyname":"Continental","salary":"100k","empid":2}]

#function for getting the user of given user id.
def get_user_by_id(id):
    for post in usersLocalArray :
      if  post['empid'] == id:
          return post
      
#function for deleting the user of given user id.
def search_by_userid(id):
    for i,post in enumerate(usersLocalArray):
      if  post['empid'] == id:
          return i


@app.get("/")
def helloworld():
    return {"fastApi": "Hi ,if you need to see more about this ,go to /docs  :-) Bye"}

# api route to return all the user's value from prostgressdb
@app.get("/users")
def read_users():
    # getting all the users from the postgress db
    cursor.execute("""select * from users""")
    post = cursor.fetchall()
    
    return {"data":post}

#api route creating a new user and storing this in List
@app.post("/users")
def read_users(user: userPost,response : Response):
    #inserting the user into prostgress database.
    cursor.execute(""" insert into users (name,age) values (%s,%s) returning *""",(user.name,user.age))
    #fetching the inserted user.
    post = cursor.fetchone()
    #need to commit the changes so that it will reflect in db
    conn.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"data": post}

#api route getting a specific  user by id
@app.get("/users/{id}")
def read_users_id(id: int,response : Response):
   #convert the id of int to str to pass in query
   #add , (str(id),) to avoid error while running big id values 
   cursor.execute(""" select * from users where empid = %s """,(str(id),))
   post =  cursor.fetchone()
   # if post is empty we are raising an exception 404 with HTTP EXception.
   if  post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user of id {id} not found in database")
      
#    if not post :
#        response.status_code = 404
#        response.status_code = status.HTTP_404_NOT_FOUND
#    else :
#        response.status_code = 200
#        response.status_code = status.HTTP_200_OK

   return {"data" : post}

#api route for delete using user id.
@app.delete("/users/{id}")
def delete_user_id(id : int):
   #deleting the user in Postgress using id.
    #add , (str(id),) to avoid error while running big id values 
   cursor.execute(""" delete from users where empid = %s returning * """,(str(id),))
   deleteindex = cursor.fetchone()
   # commit to save the changes that made
   conn.commit()

   if  deleteindex  == None :
      raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
   else:
    return {"data":f"User of {id} deleted sucessfully"}


#api route for updating the user by id.
@app.put("/users/{id}")
def update_user(id : int , userpost : userPost):
   
        cursor.execute(""" update users set name = %s , age = %s where empid = %s returning *""",(userpost.name,userpost.age,str(id),))
        updateindex = cursor.fetchone()
        conn.commit()
        if  updateindex == None :
            raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
        else:
        
            return {"data":updateindex}
    
