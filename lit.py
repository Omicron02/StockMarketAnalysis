import streamlit as st
import pandas as pd
import mysql.connector
import time
import matplotlib.pyplot as plt

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="stock"
)

cursor = cnx.cursor()

def update_chart(attribute, company, fig, ax):
    query = f'Select {attribute}, tstamp from simple_data where symbol="{company}" order by tstamp desc limit 20'
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=[attribute, 'tstamp'])
    df['tstamp'] = pd.to_datetime(df['tstamp'])
    df.set_index('tstamp', inplace=True)
    
    # Clear the previous plot and plot the new data
    ax.clear()
    ax.plot(df.index, df[attribute])
    ax.set_title(f"{attribute} vs time for {company}")
    ax.set_xlabel("Time")
    ax.set_ylabel(attribute)
    
    # Show the plot in Streamlit
    st.pyplot(fig)

symbol_dict = {"Apple": "AAPL", "Microsoft": "MSFT", "Alphabet":"GOOG", "NVIDIA":"NVDA", "Meta":"META"}

col1, col2, col3 = st.columns(3)
with col1:
    operation = st.selectbox("Select the operation:", ("Stream", "Batch"))
with col2:
    company = st.selectbox("", ("Apple", "Microsoft", "Alphabet", "Meta", "NVIDIA"))
with col3:
    attribute = st.selectbox("", ("Price", "Volume"))
if operation == "Stream":
    fig, ax = plt.subplots()
    st.title(f'Live {company} {attribute} Graph')
    update_chart(attribute, symbol_dict[company], fig, ax)
