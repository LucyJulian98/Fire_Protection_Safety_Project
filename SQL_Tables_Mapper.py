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
### Class for both overarching devices and their components
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
    Pull_Station_Quantity = Column(Integer)
    Smoke_Detector_Quantity = Column(Integer)
    Duct_Detector_Quantity = Column(Integer)

class Buildings(base) :
    __tablename__ = 'Buildings'

    Code = Column(String, primary_key = True)
    Building_Name = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)
    System_Id = Column(Integer, ForeignKey("Systems.Id"))
    System = relationship("Systems", back_populates = "Buildings")

Systems.Building = relationship("Buildings", back_populates = "Systems")

class Pad_Panels(base) :
    __tablename__ = 'Pad_Panels'

    Id = Column(Integer, primary_key = True)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    System = relationship("Systems", back_populates = "Pad_Panels")

Systems.Pads = relationship("Pad_Panels", back_populates = "Systems")

class Remote_Panels(base) :
    __tablename__ = 'Remote_Panels'

    Id = Column(Integer, primary_key = True)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    System = relationship("Systems", back_populates = "Remote_Panels") ### First argument class name, second argument table name 

Systems.Remotes = relationship("Remote_Panels", back_populates = "Systems")

### Class to create unique identifies for each device 
class Equipment_Ids(base) : 
    __tablename__ = "Equipment_Ids"

    System_Id = Column(Integer, primary_key = True) ### Unable to have foreign key constraint due to devices like hydrants and kitchen hoods 
    Building_Code = Column(String, primary_key = True) ### Unable to have foreign key constraint due to devices like hydrants 
    Device_Code = Column(String, ForeignKey('Devices.Code'), primary_key = True)    
    device = relationship("Devices", back_populates = "Equipment_Ids") ### First argument class name, second argument table name 
     
Devices.Equipment_Ids = relationship("Equipment_Ids", back_populates = "Devices")

class Latest_Inspections(base) :
    __tablename__ = "Latest_Inspections"
    
    Inspection_Id = Column(String, primary_key = True) ### From the Inspections Table 
    Inspection_Type = Column(String)
    Date = Column(String)
    System_Issues = Column(Integer)

class Inspections_Fire_Alarms(base) :
    __tablename__ = "Inspections_Fire_Alarms"

    Id = Column(String, primary_key = True)
    System_Id = Column(Integer, ForeignKey("Systems.Id"))
    Date = Column(String)
    Type = Column(String)
    Batteries_Tested = Column(Boolean)
    Pull_Stations_Tested = Column(Integer)
    Pull_Stations_Failed = Column(Integer)
    Smoke_Detectors_Tested = Column(Integer)
    Smoke_Detectors_Failed = Column(Integer)
    Duct_Detectors_Tested = Column(Integer)
    Duct_Detectors_Failed = Column(Integer)
    Source_File_Link = Column(String)
    System = relationship("Systems", back_populates = "Inspections_Fire_Alarms")

Systems.Fire_Alarm = relationship("Inspections_Fire_Alarms", back_populates = "Systems")

class Components(base) : 
    __tablename__ = "Components"

    Id = Column(String, primary_key = True)   
    Equipment_Id = Column(Integer) ### From Equipment ID Table 
    Component_Code = Column(String, ForeignKey("Devices.Code"))
    Location = Column(String)
    Address = Column(String)
    Devices = relationship("Devices", back_populates = "Components")

Devices.Components = relationship("Components", back_populates = "Devices")



base.metadata.create_all(engine)    