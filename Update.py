# import streamlit as st
# import pyodbc
# import re
# from sqlalchemy import create_engine 
# import pandas as pd

# server = 'verticaldynamix.database.windows.net'
# database = 'VerticalDynamix'
# username = 'VerticalDynamix'
# password = 'Golemw#153'
# driver = '{ODBC Driver 17 for SQL Server}'

# connection_string = f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
# conn = pyodbc.connect(connection_string)

# st.title('User Login')
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_database;UID=your_username;PWD=your_password')

# st.title('Insert Data into TargetModel Table')
# map_style = st.text_input('Map Style')
# target = st.number_input('Target', min_value=0)

# if st.button('Submit'):
#     cursor = conn.cursor()
#     sql_insert_data = '''
#     INSERT INTO TargetModel (Map_Style, Target)
#     VALUES (?, ?)
#     '''
#     cursor.execute(sql_insert_data, (map_style, target))
#     conn.commit()
#     cursor.close()
    
#     st.success('Data inserted successfully!')

import streamlit as st
import pyodbc
import threading
import time

server = 'verticaldynamix.database.windows.net'
database = 'VerticalDynamix'
username = 'VerticalDynamix'
password = 'Golemw#153'
driver = '{ODBC Driver 17 for SQL Server}'

connection_string = f"Driver={driver};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
conn = pyodbc.connect(connection_string)

# Function to insert data into the database
def insert_data():
    while True:
        # Connect to the database
        conn = pyodbc.connect(connection_string)
        
        # Define the data to insert
        model = "model"
        value = 100
        
        # Execute the insert statement
        cursor = conn.cursor()
        sql_insert_data = '''
        INSERT INTO TargetModel (Map_Style, Target)
        VALUES (?, ?)
        '''
        cursor.execute(sql_insert_data, (model, value))
        conn.commit()
        cursor.close()
        conn.close()
        
        # Sleep for 1 minute before inserting again
        time.sleep(60)

# Streamlit app
def main():
    st.title('Insert Data into TargetModel Table')

    # Button to start inserting data
    start_button = st.button("Start Inserting")

    if start_button:
        st.write("Inserting data every 1 minute...")
        # Start a new thread for the insert_data function
        insert_thread = threading.Thread(target=insert_data)
        insert_thread.start()

if __name__ == "__main__":
    main()


