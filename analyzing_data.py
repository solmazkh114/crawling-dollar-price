from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import plotly.graph_objects as go
import psycopg2



def retrieve_data(database = "rec_task", user = "postgres", table = "dollar_price"):
    password = input("Please enter your PostgreSQL password")
    connection = psycopg2.connect(user= user, password= password, database= database)
    cursor = connection.cursor()
    print("connection made")
    query = "SELECT * FROM "+ table
    df = pd.read_sql_query(query, connection)
    connection.close()
    return df


def preprocess(df):
    df['Date'] = df['Date'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
    df = df.astype({'Open': 'float', 'Close': 'float', 'Low': 'float', 'High': 'float'})
    return df

def plot(df):
    df.index = df["Date"]
    df['Close'].plot(figsize=(10, 5))
    plt.title("Close Price of Dollar in a Year")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.show()

def candlestick(df):
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
    fig.show()
