### Program to create the tables using SQL ORM

### Importing required packages 
from typing import Counter
from sqlalchemy import create_engine 
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

### Setting up the sqlite engine 
engine = create_engine("sqlite:///fps.db", echo = True)

### Declarative Base Class
base = declarative_base()

### Declaring the classes for each table 
class Buildings(base) :
    __tablename__ = 'Buildings'

    Code = Column(String, primary_key = True)
    Building_Name = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)

class Devices(base) :
    __tablename__ = 'Devices'

    Code = Column(String, primary_key = True)
    Device_Name = Column(String)

class Systems(base) :
    __tablename__ = 'Systems'

    Id = Column(Integer, primary_key = True)
    Model = Column(String)
    Mother_Board = Column(String)
    Location = Column(String)
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)

class Pad_Panels(base) :
    __tablename__ = 'Pad_Panels'

    Id = Column(Integer, primary_key = True)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    system = relationship("Systems", back_populates = "Pad_Panels")

Systems.Pads = relationship("Pad_Panels", back_populates = "Systems")

class Remote_Panels(base) :
    __tablename__ = 'Remote_Panels'

    Id = Column(Integer, primary_key = True)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    system = relationship("Systems", back_populates = "Remote_Panels") ### First argument class name, second argument table name 

Systems.Remotes = relationship("Remote_Panels", back_populates = "Systems")

### Class to create unique identifies for each device 
class Equipment_Ids(base) : 
    __tablename__ = "Equipment_Ids"

    System_Id = Column(Integer, primary_key = True) ### Unable to have foreign key constraint due to devices like hydrants 
    Building_Code = Column(String, primary_key = True) ### Unable to have foreign key constraint due to devices like hydrants 
    Device_Code = Column(String, ForeignKey('Devices.Code'), primary_key = True)    
    device = relationship("Devices", back_populates = "Equipment_Ids") ### First argument class name, second argument table name 
     
Devices.Equipment_Ids = relationship("Equipment_Ids", back_populates = "Devices")



base.metadata.create_all(engine)    