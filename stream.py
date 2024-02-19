import streamlit as st
import pandas as pd
from sqlalchemy import create_engine 
import pyodbc

server = 'verticaldynamix.database.windows.net'
database = 'VerticalDynamix'
username = 'VerticalDynamix'
password = 'Golemw#153'
driver = '{ODBC Driver 17 for SQL Server}'

st.set_page_config(
    page_title='Vertical Dynamix',
    page_icon=':)',
)
st.sidebar.success("Select report")

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

st.title("Progress Tracker")

connection_string = f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = pyodbc.connect(connection_string)

options = marketAll(conn)
selected_option = st.selectbox('Select Market', options)

data = readProgressTracker(selected_option)
UpdateDate = getLastUpdate(conn, selected_option)


if UpdateDate:
    st.write(f"Data was last updated on {UpdateDate}")
else:
    st.write("No update information available.")

if not data.empty:
    st.write("## Data Table")
    st.write(data)
else:
    st.write("No data available for the selected option.")

# Establish a connection to the SQL Server database
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')

# Streamlit UI
# st.title('Insert Data into TargetModel Table')

# Input form for Map Style
map_style = st.text_input('Map Style')

# Input form for Target
target = st.number_input('Target', min_value=0)

# Button to submit the form
if st.button('Submit'):
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Define the SQL query to insert data into the TargetModel table
    sql_insert_data = '''
    INSERT INTO TargetModel (Map_Style, Target)
    VALUES (?, ?)
    '''
    
    # Execute the SQL query
    cursor.execute(sql_insert_data, (map_style, target))
    
    # Commit the transaction
    conn.commit()
    
    # Close the cursor
    cursor.close()
    
    st.success('Data inserted successfully!')

