from sqlalchemy import Column, Integer, String

# # Uncomment this for run test
# from api_async.database import Base

# # Comment out this for run test
from database import Base


class Data1(Base):
    __tablename__ = 'data_1'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Data2(Base):
    __tablename__ = 'data_2'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class Data3(Base):
    __tablename__ = 'data_3'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
