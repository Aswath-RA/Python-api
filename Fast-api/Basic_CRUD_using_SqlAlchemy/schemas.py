from pydantic import BaseModel

class userPost(BaseModel):
    name : str
    age : int
    
class userPostResponse(userPost):
   pass

#add this Config to send the response if using sql alchemy for getting the data.
   class Config:
       orm_mode = True