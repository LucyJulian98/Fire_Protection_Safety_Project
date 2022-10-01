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


### IMPORTANT NOTE : For Foreign keys, the property names should match the table(sql) names of the referenced tables. 
### Declaring the classes for each table 

################################ SYSTEM INFRASTRUCTURE CLASSES ##################################

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
    Heat_Detector_Quantity = Column(Integer)
    Smoke_Detector_Quantity = Column(Integer)
    Duct_Detector_Quantity = Column(Integer)

class Buildings(base) :
    __tablename__ = 'Buildings'

    Code = Column(String, primary_key = True)
    Building_Name = Column(String)
    Latitude = Column(String)
    Longitude = Column(String)
   
### Class to create unique identifies for each device 
class Equipments(base) : 
    __tablename__ = "Equipments"

    Id = Column(String, primary_key = True)
    System_Id = Column(Integer) ### Can't place the foreign key constraint due to hydrants and kitchen hoods
    Building_Code = Column(String) ### Can't place the foreign key constraint due to hydrants 
    Device_Code = Column(String, ForeignKey("Devices.Code"))
    Devices = relationship("Devices", back_populates = "Equipments")

Devices.Equipments = relationship("Equipments", back_populates = "Devices")

class Components(base) : 
    __tablename__ = "Components"
  
    Id = Column(Integer, primary_key = True) ### For numbering the components within each device 
    Equipment_Id = Column(Integer, ForeignKey("Equipment_Ids.Id"), primary_key = True) ### From Equipment ID Table 
    Component_Code = Column(String, ForeignKey("Devices.Code"), primary_key = True)
    Location = Column(String)
    Address = Column(String)
    Equipments = relationship("Equipments", back_populates = "Components")
    Devices = relationship("Devices", back_populates = "Components")

Equipments.Components = relationship("Components", back_populates = "Equipments")
Devices.Components = relationship("Components", back_populates = "Devices")

class Pad_Panels(base) :
    __tablename__ = 'Pad_Panels'

    Id = Column(Integer, primary_key = True)
    Type = Column(String) ### This is where you put in PAD3 or PAD4 
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
    Equipments = relationship("Equipments", back_populates = "Hydrants")

Equipments.Hydrants = relationship("Hydrants", back_populates = "Equipments")

class Source_Files(base) :
    __tablename__ = "Source_Files"

    Id = Column(Integer, primary_key = True)
    Equipment_Id = Column(String, ForeignKey("Equipment_Ids.Id")) ### The equipment it belongs to 
    Link = Column(String)
    Equipments = relationship("Equipments", back_populates = "Source_Files")

Equipments.Source_Files = relationship("Source_Files", back_populates = "Equipments")


################################ INSPECTION CLASSES ##################################

class Inspections(base) :
    __tablename__ = "Inspections"

    Id = Column(String, primary_key = True) ### To be automated and generated every time a record is entered 
    Equipment_Id = Column(String, ForeignKey("Equipment_Ids.Id"))
    Date = Column(String)
    Type = Column(String)
    Source_File_Link_Id = Column(Integer, ForeignKey(Source_Files.Id))
    Equipments = relationship("Equipments", back_populates = "Inspections")
    Source_Files = relationship("Source_Files", back_populates = "Inspections")

Equipments.Inspections = relationship("Inspections", back_populates = "Equipments")
Source_Files.Inspections = relationship("Inspections", back_populates = "Source_Files")

class Inspections_Fire_Alarms(base) :
    __tablename__ = "Inspections_Fire_Alarms"

    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
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

    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
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

    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Fire_Pump_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Fire_Pumps")

Inspections.Inspections_Fire_Pumps = relationship("Inspections_Fire_Pumps", back_populates = "Inspections")

class Inspections_Hydrants(base) :
    __tablename__ = "Inspections_Hydrants"

    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Hydrant_Testing_Problems = Column(String) ### Ideally yes or no.     
    Inspections = relationship("Inspections", back_populates = "Inspections_Hydrants")

Inspections.Inspections_Hydrants = relationship("Inspections_Hydrants", back_populates = "Inspections")

### For FM-200, Foam, Kitchen Hoods, Vesdas? 
class Inspections_Special_Protection_Systems(base) : 
    __tablename__ = "Inspections_Special_Protection_Systems"

    Inspection_Id = Column(String, ForeignKey("Inspections.Id"), primary_key = True)
    Testing_Problems = Column(Integer)
    Inspections = relationship("Inspections", back_populates = "Inspections_Special_Protection_Systems")

Inspections.Inspections_Special_Protection_Systems = relationship("Inspections_Special_Protection_Systems", back_populates = "Inspections")



################################ TESTS AND FAILURES ##################################

class Tests(base) :
    __tablename__ = "Tests"

    Id = Column(Integer, primary_key = True)
    Testing_Parameter = Column(String)
    ITM_Code = Column(String)


### Can't have compositie primary key made of Inpection Id and Test Id because different comoponents of fire alarm may fail in same test and inspection 
class Failures(base) :
    __tablename__ = "Failures"
    
    Id = Column(String, primary_key = True) ##uuid? 
    Inspection_Id = Column(String, ForeignKey("Inspections.Id"))
    Test_Id = Column(Integer, ForeignKey("Tests.Id"))
    Component_Id = Column(String, ForeignKey("Components.Id")) ### Not part of the primary key because device such as hydrants don't have a component
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

