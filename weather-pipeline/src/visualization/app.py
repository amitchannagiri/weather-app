import streamlit as st
import pandas as pd
import duckdb
import plotly.express as px

# Database connection function
def get_db_connection(db_name: str = "weather.duckdb"):
    """Establishes a connection to the DuckDB database."""
    try:
        conn = duckdb.connect(db_name)
        return conn
    except Exception as e:
        st.error(f"Error connecting to DuckDB database: {e}")
        return None

# Data loading functions
def load_data(conn, table_name: str):
    """Loads data from a specified table in the DuckDB database."""
    try:
        query = f"SELECT * FROM {table_name}"
        df = conn.execute(query).fetchdf()
        return df
    except Exception as e:
        st.error(f"Error loading data from table {table_name}: {e}")
        return None

def load_gold_data(conn):
    """Loads gold data and format the date"""
    try:
        query = f"SELECT * FROM city_weather"
        df = conn.execute(query).fetchdf()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading data from gold layer: {e}")
        return None

# Streamlit app starts here
st.set_page_config(page_title="Weather Data Dashboard", layout="wide")
st.title("Weather Data Dashboard")

# Connect to DuckDB
conn = get_db_connection()

if conn:
    # Data selection
    st.sidebar.header("Data Selection")
    table_names = ["weather_data_bronze", "weather_data_silver", "weather_data_gold"]
    selected_table = st.sidebar.selectbox("Select Data Layer:", table_names)

    # Load data
    if selected_table == "weather_data_gold":
        df = load_gold_data(conn)
    else:
        df = load_data(conn, selected_table)

    if df is not None:
        st.subheader(f"Data from {selected_table}")
        st.dataframe(df)

        # Plotting if it's gold data
        if selected_table == "weather_data_gold":
             # Create a line chart using Plotly Express
            fig = px.line(df, x='timestamp', y=['main_temp', 'main_feels_like', 'main_temp_min', 'main_temp_max'],
                         labels={'value': 'Temperature', 'timestamp': 'Timestamp'},
                         title='Temperature Over Time')

            # Update layout for better readability
            fig.update_layout(legend_title_text='Temperature Types')

            # Display the chart using Streamlit
            st.plotly_chart(fig, use_container_width=True)

        # Show statistics for numeric columns
        if selected_table != "weather_data_bronze":
            st.subheader("Descriptive Statistics")
            numeric_df = df.select_dtypes(include=['number'])
            st.dataframe(numeric_df.describe())
    else:
        st.warning("No data available or an error occurred.")

    conn.close()