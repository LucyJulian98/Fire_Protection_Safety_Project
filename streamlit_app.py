### Streamlit App 
import streamlit as st 
import sqlite3
import pandas as pd

conn = sqlite3.connect("fps.db")


st.sidebar.markdown("### Fire Protection and Safety Mock Database")
st.sidebar.markdown("This is a trial app looking at extracting and joining tables from the local database.")
Options = ["Home", "System Specifications", "Latest Inspection Reports", "Building wise Inspections", "Building Overview", "Deficiency Graphs", "Inspection_Updates"]
option = st.sidebar.selectbox("Select an Option", Options)

if option == "Home" :
    st.title("Welcome to FPS Database")
    st.subheader("Choose options on the sidebar.")

elif option == "System Specifications" :
    df_buildings = pd.read_sql("SELECT * FROM Buildings", con = conn)
    buildings_options = list(df_buildings.Building_Name)
    df_systems = pd.read_sql("SELECT * FROM SYSTEMS", con = conn)
    building = st.selectbox("Select a building", buildings_options)
    df_build_system = pd.merge(df_systems, df_buildings, left_on = 'Id', right_on = 'System_Id')  
    st.write("Model :" , df_build_system.Model) 
    st.write("Mother Board : ", df_build_system.Mother_Board)
    st.write("Location : ", df_build_system.Location)
    st.write("Battery Capacity : ", df_build_system.Battery_Specs)
    st.write("Battery Installed Date : ", df_build_system.Battery_Date)
    st.write("Pull Stations : ", df_build_system.Pull_Station_Quantity)
    st.write("Smoke Detectors : ", df_build_system.Smoke_Detector_Quantity)
    st.write("Duct Detectors : ", df_build_system.Duct_Detector_Quantity)

elif option == "Latest Inspection Reports"  :
    df_latest_report = pd.read_sql("SELECT * FROM Latest_Inspections", con = conn)
    st.write(df_latest_report)  

elif option == "Building wise Inspections" :
    df_buildings = pd.read_sql("SELECT * FROM Buildings", con = conn)
    buildings_options = list(df_buildings.Building_Name)
    building = st.selectbox("Select a building", buildings_options) 
    df_inspections = pd.read_sql("SELECT * FROM Inspections_Fire_Alarms", con = conn)
    st.write(df_inspections)