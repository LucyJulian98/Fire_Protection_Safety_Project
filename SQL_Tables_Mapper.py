### Program to create the tables using SQL ORM

### Importing required packages 
import sqlalchemy 
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

### Setting up the sqlite engine 
engine = sqlalchemy.create_engine("sqlite:///fps.db", echo = True)

### Declarative Base Class
base = declarative_base()

### Declaring the classes for each table 
class Buildings(base) :
    __tablename__ = 'Buildings'

    Code = Column(Integer, primary_key = True)
    Building_Name = Column(String)

base.metadata.create_all(engine)    