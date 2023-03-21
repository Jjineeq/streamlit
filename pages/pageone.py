import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title("PCA를 진행해보자")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    st.write(df)
    df.head(10)
    df2 = df[df['지점명']=='속초']
    
    g1, g2, g3 = st.columns((1,1,1))   

    fig = px.line(df2, x = '일시', y='기온(°C)', template = 'seaborn')
    
    fig.update_traces(marker_color='#264653')
    
    fig.update_layout(title_text="기온",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g2.plotly_chart(fig, use_container_width=True) 
    