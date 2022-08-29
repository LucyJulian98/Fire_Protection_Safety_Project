### Program to create the tables using SQL ORM

### Importing required packages 
import sqlalchemy 

### Setting up the sqlite engine 
engine = sqlalchemy.create_engine("sqlite://FPS.db", echo = True)

### Declarative Base Class
base = sqlalchemy.ext.declarative.declarative_base()

### Declaring the classes for each table 
