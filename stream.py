import streamlit as st
import pandas as pd

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
    data = {
        'Name': ['John', 'Alice', 'Bob', 'Jane'],
        'Age': [25, 30, 35, 40],
        'Location': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    main()
