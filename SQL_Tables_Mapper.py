### Program to create the tables using SQL ORM

### Importing required packages 
from typing import Counter
from sqlalchemy import create_engine 
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

### Setting up the sqlite engine 
engine = create_engine("sqlite:///fps.db", echo = True)

### Declarative Base Class
base = declarative_base()


### IMPORTANT NOTE : For Foerign keys, the property names should match the table(sql) names of the referenced tables. 
### Declaring the classes for each table 

################################ SYSTEM INFRASTRUCTURE CLASSES ##################################
### Class to create unique identifies for each device 
class Equipment_Ids(base) : 
    __tablename__ = "Equipment_Ids"

    Id = Column(String, primary_key = True)


class Devices(base) :  
    __tablename__ = 'Devices'

    Code = Column(String, primary_key = True)
    Device_Name = Column(String)

class Components(base) : 
    __tablename__ = "Components"

    Id = Column(String, primary_key = True)   
    Equipment_Id = Column(Integer) ### From Equipment ID Table 
    Component_Code = Column(String, ForeignKey("Devices.Code"))
    Location = Column(String)
    Address = Column(String)
    Devices = relationship("Devices", back_populates = "Components")

Devices.Components = relationship("Components", back_populates = "Devices")

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
    Heat_Detector_Quantity = Column(Integer)
    Smoke_Detector_Quantity = Column(Integer)
    Duct_Detector_Quantity = Column(Integer)

class Buildings(base) :
    __tablename__ = 'Buildings'

    Code = Column(String, primary_key = True)
    Building_Name = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)
    System_Id = Column(Integer, ForeignKey("Systems.Id"))
    Systems = relationship("Systems", back_populates = "Buildings")

Systems.Buildings = relationship("Buildings", back_populates = "Systems")

class Pad_Panels(base) :
    __tablename__ = 'Pad_Panels'

    Id = Column(Integer, primary_key = True)
    Type = Column(String)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    Systems = relationship("Systems", back_populates = "Pad_Panels")

Systems.Pad_Panels = relationship("Pad_Panels", back_populates = "Systems")

class Remote_Panels(base) :
    __tablename__ = 'Remote_Panels'

    Id = Column(Integer, primary_key = True)
    Location = Column(String)
    System_Id = Column(Integer, ForeignKey('Systems.Id'))
    Battery_Quantity = Column(Integer)
    Battery_Specs = Column(String)
    Battery_Date = Column(String)
    Systems = relationship("Systems", back_populates = "Remote_Panels") ### First argument class name, second argument table name 

Systems.Remote_Panels = relationship("Remote_Panels", back_populates = "Systems")

class Hydrants(base) :
    __tablename__ = "Hydrants"

    Id = Column(String, ForeignKey("Equipment_Ids.Id"), primary_key = True)
    Location = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)
    Equipment_Ids = relationship("Equipment_Ids", back_populates = "Hydrants")

Equipment_Ids.Hydrants = relationship("Hydrants", back_populates = "Equipment_Ids")

class Source_Files(base) :
    __tablename__ = "Source_Files"

    Id = Column(Integer, primary_key = True)
    Device_Code = Column(String, ForeignKey(Devices.Code))
    Link = Column(String)
    Devices = relationship("Devices", back_populates = "Source_Files")

Devices.Source_Files = relationship("Source_Files", back_populates = "Devices")


################################ INSPECTION CLASSES ##################################

### To be populated using triggers or pandas 
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
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Systems = relationship("Systems", back_populates = "Inspections_Fire_Alarms")
    Source_Files = relationship("Source_Files", back_populates = "Inspections_Fire_Alarms")

Systems.Inspections_Fire_Alarms = relationship("Inspections_Fire_Alarms", back_populates = "Systems")
Source_Files.Inspections_Fire_Alarms = relationship("Inspections_Fire_Alarms", back_populates = "Source_Files")

class Inspections_Sprinklers(base) :
    __tablename__ = "Inspections_Sprinklers"

    Id = Column(String, primary_key = True)
    System_Id = Column(Integer, ForeignKey("Systems.Id"))
    Date = Column(String)
    Type = Column(String)
    Dry_System_Problems = Column(Integer)
    Dry_Pipe_Valve_Problems = Column(Integer)
    Air_Compressor_Problems = Column(Integer)
    Wet_Check_Valve_Problems = Column(Integer)
    Wet_System_Problems = Column(Integer)
    Control_Valve_Problems = Column(Integer)
    Supervisory_Devices_Problems = Column(Integer)
    Alarm_Devices_Problems = Column(Integer)
    FDC_Problems = Column(Integer)
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Systems = relationship("Systems", back_populates = "Inspections_Sprinklers")
    Source_Files = relationship("Source_Files", back_populates = "Inspections_Sprinklers")

Systems.Inspections_Sprinklers = relationship("Inspections_Sprinklers", back_populates = "Systems")
Source_Files.Inspections_Sprinklers = relationship("Inspections_Sprinklers", back_populates = "Source_Files")

class Inspections_Fire_Pumps(base) :
    __tablename__ = "Inspections_Fire_Pumps"

    Id = Column(String, primary_key = True)
    Equipment_Id = Column(Integer, ForeignKey("Equipment_Ids.Id"))
    Date = Column(String)
    Type = Column(String)
    Fire_Pump_Problems = Column(Integer)
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Equipment_Ids = relationship("Equipment_Ids", back_populates = "Inpections_Fire_Pumps")
    Source_Files = relationship("Source_Files", back_populates = "Inspections_Fire_Pumps")

Equipment_Ids.Inspections_Fire_Pumps = relationship("Inspections_Fire_Pumps", back_populates = "Equipment_Ids")
Source_Files.Inspections_Fire_Pumps = relationship("Inspections_Fire_Pumps", back_populates = "Source_Files")

class Inspections_Hydrants(base) :
    __tablename__ = "Inspections_Hydrants"

    Id = Column(String, primary_key = True)
    Hydrant_Id = Column(Integer, ForeignKey("Hydrants.Id"))
    Date = Column(String)
    Type = Column(String)
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Hydrants = relationship("Hydrants", back_populates = "Inspections_Hydrants")
    Source_Files = relationship("Source_Files", back_populates = "Inspections_Hydrants")

Hydrants.Inspections_Hydrants = relationship("Inpections_Hydrants", back_populates = "Hydrants")
Source_Files.Inspections_Hydrants = relationship("Inspections_Hydrants", back_populates = "Source_Files")

################################ TESTS AND FAILURES ##################################

class Tests(base) :
    __tablename__ = "Tests"

    Id = Column(Integer, primary_key = True)
    Testing_Parameter = Column(String)
    ITM_Code = Column(String)

class Failures(base) :
    __tablename__ = "Failures"

    Component_Id = Column(String, ForeignKey("Components.Id"), primary_key = True)
    Inpsection_Id = Column(String, primary_key = True)
    Test_Id = Column(Integer, ForeignKey("Tests.Id"), primary_key = True)
    Technician_Note = Column(String)
    Components = relationship("Components", back_populates = "Failures")
    Tests = relationship("Tests", back_populates = "Failures")

Components.Failures = relationship("Failures", back_populates = "Components")
Tests.Failures = relationship("Failures", back_populates = "Tests")

### Create the tables in the database 
base.metadata.create_all(engine)   

### Creating session
#session = sessionmaker(bind = engine)
#session = session()
#record = Devices(Code = "HD", Device_Name = "Heat Detector")

### Populating the Devices Table 
#session.add(record)
#session.commit()

