

import numpy as np
import pandas as pd

import openpyxl 
import datetime as dt

import seaborn as sns
import plotly.graph_objects as Dash
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st


def consulta_bcb(codigo_bcb):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_bcb}/dados?formato=json"

    df = pd.read_json(url)
    df['data'] = pd.to_datetime(df['data'], dayfirst=True)
    df.set_index('data', inplace= True)
    return df

Desemprego = consulta_bcb(24369)

Desemprego['Média móvel'] = Desemprego['valor'].rolling(window=5).mean()

fig = Dash.Figure()

fig.add_trace(Dash.Scatter(
    x=Desemprego.index,
    y=Desemprego['valor'],
    mode='lines',
    name='Taxa Desocupação', 
    line=dict(color='blue')  
))

fig.add_trace(Dash.Scatter(
    x=Desemprego.index,
    y=Desemprego['Média móvel'],
    mode='lines',
    name='MM5', 
    line=dict(color='red')  
))


fig.update_layout(
    title='Evolução Mensal da Taxa de desocupação (%) - Desemprego',
    xaxis_title='Período',
    yaxis_title='Valor',
    legend_title='Legenda'
)   

st.title('Desemprego no Período')
st.plotly_chart(fig)