from typing import Union
from typing import Optional

from fastapi import FastAPI ,Response,status,HTTPException
from pydantic import BaseModel
import random
app = FastAPI()

class userPost(BaseModel):
    name : str
    age : int
    role : str
    companyname : Optional[str] = None
    salary : str = "No Value"


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

# api route to return all the user's value in the list
@app.get("/users")
def read_users():
    return {"data":usersLocalArray}

#api route creating a new user and storing this in List
@app.post("/users")
def read_users(user: userPost,response : Response):
    user_dict = user.dict()
    user_dict['empid'] = random.randrange(0,999)
    usersLocalArray.append(user_dict)
    response.status_code = status.HTTP_201_CREATED
    return {"data": user_dict}

#api route getting a specific  user by id
@app.get("/users/{id}")
def read_users_id(id: int,response : Response):
   print(id)
   print(type(id))
   post =  get_user_by_id(id)
   # if post is empty we are raising an exception 404 with HTTP EXception.
   if not post:
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
   #getting the index needed to delete the user.
   deleteindex = search_by_userid(id)
   if  deleteindex  == None :
      raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
   else:
    usersLocalArray.pop(deleteindex)
   return {"data":f"User of {id} deleted sucessfully"}


#api route for updating the user by id.
@app.put("/users/{id}")
def update_user(id : int , userpost : userPost):
    updateindex = search_by_userid(id)
    print(updateindex)
    if  updateindex == None :
      raise HTTPException(status_code=404,detail=f"user of {id} is not available in database")
    else:
     print(usersLocalArray[updateindex])
     updatePost = userpost.dict()
     updatePost['empid'] = id
     usersLocalArray[updateindex] = updatePost
    return {"data":updatePost}
