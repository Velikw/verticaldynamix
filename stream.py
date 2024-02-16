import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 
import pyodbc

server = 'verticaldynamix.database.windows.net'
database = 'VerticalDynamix'
username = 'VerticalDynamix'
password = 'Golemw#153'
driver = '{ODBC Driver 17 for SQL Server}'

def getLastUpdate(conn, Market):
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT TOP 1 eventDate, eventTime
        FROM EventUpdateTB
        WHERE Market = ?
        ORDER BY eventDate DESC, eventTime DESC
        """,
        (Market,)
    )
    row = cursor.fetchone()
    if row:
        event_date, event_time = row
        return f"{event_date.strftime('%Y-%m-%d')} at {event_time.strftime('%H:%M')}"
    else:
        return None

def marketAll(conn):
    results=[]
    cursor=conn.cursor()
    cursor.execute(
        """select MarketName from MarketID order by MarketName ASC"""
    )
    for row in cursor:
        results.append(list(row)[0])
    return results

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
    st.title("Progress Tracker")

        # Establish database connection
    
    connection_string = f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conn = pyodbc.connect(connection_string)

    # connection_string = 'mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server'
    # engine = create_engine(connection_string)

    options = marketAll(conn)
    selected_option = st.selectbox('Select Market', options)

    # st.write('Selected Options:', selected_option)
     # Load data for the selected option
    data = readProgressTracker(selected_option)

    UpdateDate = getLastUpdate(conn, selected_option)
    # date_str, time_str = UpdateDate
    # st.write(f"Data was last updated on date: {date_str} at time: {time_str}")


    if UpdateDate:
        st.write(f"Data was last updated on {UpdateDate}")
    else:
        st.write("No update information available.")

    # Display data tablef
    if not data.empty:
        st.write("## Data Table")
        st.write(data)
    else:
        st.write("No data available for the selected option.")

# def load_data():
#     # Sample data
#     # data = {
#     #     'Name': ['John', 'Alice', 'Bob', 'Jane'],
#     #     'Age': [25, 30, 35, 40],
#     #     'Location': ['New York', 'Los Angeles', 'Chicago', 'Houston']
#     # }
#     data=readProgressTracker('Duluth')
#     df = pd.DataFrame(data)
#     return df

if __name__ == "__main__":
    main()
