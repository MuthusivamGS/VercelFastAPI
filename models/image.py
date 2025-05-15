
from sqlalchemy import Column, Integer, String, LargeBinary
from db.database import Base
from pydantic import BaseModel
class Image(Base):
    __tablename__= "images2"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    group = Column(String)
    data = Column(LargeBinary)
class imageSchema(BaseModel):
    id: int
    name: str
    description: str
    group: str
    data: str
    class Config:
        orm_mode = True
