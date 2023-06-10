from typing import Union
from typing import Optional
from fastapi import FastAPI ,Response,status,HTTPException,Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import random
import time
import  model
from schemas import userPost,userPostResponse
from database import  engine,get_db
from sqlalchemy.orm import Session




app = FastAPI()
model.Base.metadata.create_all(bind=engine)


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




@app.get("/sys")
def helloworld(db: Session = Depends(get_db)):
    return {"fastApi": "Hi ,if you need to see more about this ,go to /docs  :-) Bye"}

# api route to return all the user's value from prostgressdb
@app.get("/users")
def read_users(db: Session = Depends(get_db)):
    # getting all the users from the postgress db using sqlalchemy
    # cursor.execute("""select * from users""")
    # post = cursor.fetchall()
    post =  db.query(model.User).all()
    
    return {"data":post}



#api route creating a new user and storing this in List
@app.post("/users",response_model=userPostResponse)
def read_users(user: userPost,response : Response,db: Session = Depends(get_db)):
   
#inserting a new element to postgress using sqlalchemy 
# ** means unpacking the dict and sending direcly to it.
    new_post =  model.User(**user.dict())
    db.add(new_post) # adding to db
    db.commit() # commiting the changes to db
    db.refresh(new_post) # save the updated value to return as response.
    
    
    response.status_code = status.HTTP_201_CREATED
    return new_post




#api route getting a specific  user by id
@app.get("/users/{id}")
def read_users_id(id: int,db: Session = Depends(get_db)):
   
   getone_post = db.query(model.User).filter(model.User.empid == id).first()

   # if post is empty we are raising an exception 404 with HTTP EXception.
   if getone_post == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user of id {id} not found in database")
      
   return {"data" : getone_post}




#api route for delete using user id.
@app.delete("/users/{id}")
def delete_user_id(id : int,db: Session = Depends(get_db)):
   #deleting the user in Postgress using sqlalchemy with  id.
    deleted_post = db.query(model.User).filter(model.User.empid == id)


    if  deleted_post.first()  == None :
      raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
    else:
    # for deleting set this synchronize_session=False
        deleted_post.delete(synchronize_session=False)
        db.commit() # commiting the changes to db

        return {"data":f"User of {id} deleted sucessfully"}





#api route for updating the user by id.
@app.put("/users/{id}")
def update_user(id : int , userpost : userPost,db: Session = Depends(get_db)):
   
        retrive_post = db.query(model.User).filter(model.User.empid == id)

        update_post =  retrive_post.first()
        if  update_post == None :
            raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
        else:
            retrive_post.update(userpost.dict(),synchronize_session=False)
            db.commit()
           

            return {"data":retrive_post.first()}
    
