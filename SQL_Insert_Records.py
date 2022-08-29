### Program to insert records into the fps database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SQL_Tables_Mapper import Devices
### Connecting to the sqlite engine 
engine = create_engine("sqlite:///fps.db", echo = True)

### Creating session
session = sessionmaker(bind = engine)

record = Devices(Code = "FA", Name = "Fire Alarm")

### Populating the Devices Table 
session.add(record)
session.commit()