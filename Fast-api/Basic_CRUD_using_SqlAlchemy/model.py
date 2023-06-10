from sqlalchemy import Boolean, Column, Integer, String


from database import Base

class User(Base):
    __tablename__ = "users"

    empid = Column(Integer, primary_key=True,nullable = False)
    name   = Column(String,nullable = False)
    age =  Column(Integer,nullable = False)

