import streamlit as st
import pandas as pd
import mysql.connector
import time
import matplotlib.pyplot as plt
import datetime
import matplotlib.ticker as ticker

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="stock"
)

cursor = cnx.cursor()

def simple_chart(attribute, company, fig, ax):

    query = f'Select {attribute}, tstamp from simple_data where symbol="{company}" order by tstamp desc limit 30'
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[attribute, 'tstamp'])
    df['tstamp'] = pd.to_datetime(df['tstamp'])
    df.set_index('tstamp', inplace=True)
    
    ax.clear()
    ax.plot(df.index, df[attribute], marker = "o")
    ax.set_title(f"{attribute} vs time for {company}")
    ax.set_xlabel("Time")
    ax.set_ylabel(attribute)
    
    st.pyplot(fig)

def agg_chart(attribute, company, fig, ax):
    query = f'Select {attribute}_avg, {attribute}_min, {attribute}_max, end_time from agg_data where symbol = "{company}" order by end_time desc limit 30'
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[f'{attribute}_avg', f'{attribute}_min', f'{attribute}_max', 'end_time'])
    df['end_time'] = pd.to_datetime(df["end_time"])
    df.set_index('end_time', inplace=True)

    ax.clear()
    ax.plot(df.index, df[f'{attribute}_avg'], label=f'Avg {attribute}', marker = "o")
    ax.plot(df.index, df[f'{attribute}_min'], label=f'Min {attribute}', marker = "*")
    ax.plot(df.index, df[f'{attribute}_max'], label=f'Max {attribute}', marker = "d")
    ax.set_title(f"{attribute} Min/Max/Avg vs Time")
    ax.set_xlabel("Time")
    ax.set_ylabel(attribute)
    ax.legend()

    st.pyplot(fig)

def batch_process(company, start, end):
    query = f'select avg(price) as avg_price, min(price) as min_price, max(price) as max_price, avg(volume) as avg_volume, max(volume) as max_volume, min(volume) as min_volume from simple_data where tstamp between "{start}" and "{end}" and symbol = "{company}" ' 
    cursor.execute(query)
    data = cursor.fetchall()
    avg_price, min_price, max_price, avg_volume, max_volume, min_volume = data[0]
    st.subheader(f"Data between {start} and {end}:")
    st.write(f"Average Price: {avg_price}")
    st.write(f"Max Price: {max_price}")
    st.write(f"Min Price: {min_price}")
    st.write(f"Average Volume: {avg_volume}")
    st.write(f"Max Volume: {max_volume}")
    st.write(f"Min Volume: {min_volume}")

symbol_dict = {"Apple": "AAPL", "Microsoft": "MSFT", "Alphabet":"GOOG", "NVIDIA":"NVDA", "Meta":"META"}

col1, col2, col3, col4 = st.columns(4)
with col1:
    operation = st.selectbox("Processing:", ("Stream", "Batch"))
with col2:
    company = st.selectbox("Company:", ("Apple", "Microsoft", "Alphabet", "Meta", "NVIDIA"))
with col3:
    if operation == "Stream":
        attribute = st.selectbox("Attribute:", ("Price", "Volume"))
    else:
        start_date = st.date_input("Start Date:")
        start_time = st.time_input("Start Time:", step = 300)
with col4:
    if operation == "Stream":
        agg = st.selectbox("Type:", ("Simple", "Aggregated"))
    else:
        end_date = st.date_input("End Date:")
        end_time = st.time_input("End Time:", step = 300)
if operation == "Stream":
    width = st.sidebar.slider("plot width", 1, 25, 10)
    height = st.sidebar.slider("plotheight", 1, 25, 7)

    fig, ax = plt.subplots(figsize = (width,height))
    st.title(f'{agg} {company} {attribute} Graph')
    if agg == "Simple":
        simple_chart(attribute, symbol_dict[company], fig, ax)
    else:
        agg_chart(attribute, symbol_dict[company], fig, ax)
elif operation == "Batch":
        st.title("Batch Processing Output")
        start_date_query = datetime.datetime.combine(start_date, start_time).strftime('%Y-%m-%d %H:%M:%S')
        end_date_query = datetime.datetime.combine(end_date, end_time).strftime('%Y-%m-%d %H:%M:%S')

        batch_process(symbol_dict[company], start_date_query, end_date_query)


    
