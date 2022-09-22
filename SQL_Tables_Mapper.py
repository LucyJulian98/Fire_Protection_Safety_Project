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

### Class to create unique identifies for each device 
class Equipment_Ids(base) : 
    __tablename__ = "Equipment_Ids"

    Id = Column(String, primary_key = True)
    System_Id = Column(Integer) ### Can't place the foreign key constraint due to hydrants and kitchen hoods
    Building_Code = Column(String) ### Can't place the foreign key constraint due to hydrants 
    Device_Code = Column(String, ForeignKey("Devices.Code"))
    Devices = relationship("Devices", back_populates = "Equipment_Ids")

Devices.Equipments_Ids = relationship("Equipment_Ids", back_populates = "Devices")

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

class Inspections(base) :
    __tablename__ = "Inspections"

    Id = Column(String, primary_key = True) ### To be automated and generated every time a record is entered 
    Equipment_Id = Column(String, ForeignKey("Equipment_Ids.Id"))
    Date = Column(String)
    Type = Column(String)
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Equipment_Ids = relationship("Equipment_Ids", back_populates = "Inspections")
    Source_Files = relationship("Source_Files", back_populates = "Inspections")

Equipment_Ids.Inspections = relationship("Inspections", back_populates = "Equipment_Ids")
Source_Files.Inspections = relationship("Inspections", back_populates = "Source_Files")

class Inspections_Fire_Alarms(base) :
    __tablename__ = "Inspections_Fire_Alarms"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Batteries_Tested = Column(Boolean)
    Heat_Detectors_Tested = Column(Integer)
    Heat_Detectors_Failed = Column(Integer)
    Pull_Stations_Tested = Column(Integer)
    Pull_Stations_Failed = Column(Integer)
    Smoke_Detectors_Tested = Column(Integer)
    Smoke_Detectors_Failed = Column(Integer)
    Duct_Detectors_Tested = Column(Integer)
    Duct_Detectors_Failed = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Fire_Alarms")

Inspections.Inspections_Fire_Alarms = relationship("Inspections_Fire_Alarms", back_populates = "Inspections")

class Inspections_Sprinklers(base) :
    __tablename__ = "Inspections_Sprinklers"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Dry_System_Problems = Column(Integer)
    Dry_Pipe_Valve_Problems = Column(Integer)
    Air_Compressor_Problems = Column(Integer)
    Wet_Check_Valve_Problems = Column(Integer)
    Wet_System_Problems = Column(Integer)
    Control_Valve_Problems = Column(Integer)
    Supervisory_Devices_Problems = Column(Integer)
    Alarm_Devices_Problems = Column(Integer)
    FDC_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Sprinklers")

Inspections.Inspections_Sprinklers = relationship("Inspections_Sprinklers", back_populates = "Inspections")

class Inspections_Fire_Pumps(base) :
    __tablename__ = "Inspections_Fire_Pumps"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Fire_Pump_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Fire_Pumps")

Inspections.Inspections_Fire_Pumps = relationship("Inspections_Fire_Pumps", back_populates = "Inspections")

class Inspections_Hydrants(base) :
    __tablename__ = "Inspections_Hydrants"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Hydrant_Testing_Problems = Column(String) ### Ideally yes or no.     
    Inspections = relationship("Inspections", back_populates = "Inspections_Hydrants")

Inspections.Inspections_Hydrants = relationship("Inspections_Hydrants", back_populates = "Inspections")

class Inspections_Foam_Systems(base) :
    __tablename__ = "Inspections_Foam_Systems"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Foam_Testing_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Foam_Systems")

Inspections.Inspections_Foam_Systems = relationship("Inspections_Foam_Systems", back_populates = "Inspections")

class Inspections_FM_200(base) :
    __tablename__ = "Inspections_FM_200"

    Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    FM_Testing_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_FM_200")

Inspections.Inspections_FM_200 = relationship("Inspections_FM_200", back_populates = "Inspections")


'''
### To be populated using triggers or pandas 
class Latest_Inspections(base) :
    __tablename__ = "Latest_Inspections"
    
    Inspection_Id = Column(String, primary_key = True) ### From the Inspections Table 
    Inspection_Type = Column(String)
    Date = Column(String)
    System_Issues = Column(Integer)
'''


################################ TESTS AND FAILURES ##################################

class Tests(base) :
    __tablename__ = "Tests"

    Id = Column(Integer, primary_key = True)
    Testing_Parameter = Column(String)
    ITM_Code = Column(String)

class Failures(base) :
    __tablename__ = "Failures"
    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Component_Id = Column(String, ForeignKey("Components.Id"), primary_key = True)
    Test_Id = Column(Integer, ForeignKey("Tests.Id"), primary_key = True)
    Technician_Note = Column(String)
    Inspections = relationship("Inspections", back_populates = "Failures")
    Components = relationship("Components", back_populates = "Failures")
    Tests = relationship("Tests", back_populates = "Failures")

Inspections.Failures = relationship("Failures", back_populates = "Inspections")
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

