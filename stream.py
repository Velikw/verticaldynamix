import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 

server = 'verticaldynamix.database.windows.net'
database = 'VerticalDynamix'
username = 'VerticalDynamix'
password = 'Golemw#153'
driver = '{ODBC Driver 17 for SQL Server}'


def readProgressTracker(Market):
    connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
    engine = create_engine(connection_string)
    query = """SELECT ID,LCP_name,Pole_Count,F_Status,F_QC,F_Recollects,QC_User,Photos_Classified,ID_Tags_Status,
    MRE_Status,Packet_Status,ID_Tags_User,MRE_User,QC_User_Final,CommentTracking 
    from EngProgressTracking WHERE Market = ?"""
    try:
        df = pd.read_sql_query(query, engine, params=[(Market,)])
    except Exception as e:
        print(f"Error occurred: {e}")
        df = pd.DataFrame() 
    return df

def main():
    # Title
    st.title("Simple Dashboard")

    # Load data
    data = load_data()

    # Display data table
    st.write("## Data Table")
    st.write(data)

def load_data():
    # Sample data
    # data = {
    #     'Name': ['John', 'Alice', 'Bob', 'Jane'],
    #     'Age': [25, 30, 35, 40],
    #     'Location': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    # }
    data=readProgressTracker('Duluth')
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    main()
