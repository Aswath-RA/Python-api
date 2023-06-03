from typing import Union
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import random
app = FastAPI()

class userpost(BaseModel):
    name : str
    age : int
    role : str
    companyname : Optional[str] = None
    salary : str = "No Value"


usersLocalArray = [{"name":"Aswath","age" : 23,"role":"ios Developer","companyname":"Vrdella","salary":"20k","empid":1},{"name":"John","age" : 30,"role":"Hitman","companyname":"Continental","salary":"100k","empid":2}]

def get_user_by_id(id):
    for post in usersLocalArray :
      if  post['empid'] == id:
          return post
      

@app.get("/")
def helloworld():
    return {"fastApi": "Hi ,if you need to see more about this ,go to /docs  :-) Bye"}

# to return all the user's value in the list
@app.get("/users")
def read_users():
    return {"data":usersLocalArray}

#creating a new user and storing this in List
@app.post("/users")
def read_users(user: userpost):
    user_dict = user.dict()
    user_dict['empid'] = random.randrange(0,999)
    usersLocalArray.append(user_dict)
    return {"data": user_dict}

#getting a specific  user by id
@app.get("/users/{id}")
def read_users_id(id: int):
   print(id)
   print(type(id))
   post =  get_user_by_id(id)
   return {"data" : post}

