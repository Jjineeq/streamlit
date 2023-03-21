import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title("지점을 선택해서 확인해보자")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
    branch = df.지점명.unique()
    branch = branch.reshape(5,-1)
    st.write('지점 목록 : ',branch)
    select = st.text_input('원하는 곳을 입력 : ')
    df2 = df[df['지점명']== select]
    df2 = df2.sort_values(['지점명','일시'])
    g1, g2, g3 = st.columns((1,1,1))   

    fig = px.line(df2, x = '일시', y='기온', template = 'seaborn')
    
    fig.update_traces(marker_color='#264653')
    
    fig.update_layout(title_text="기온",title_x=0,margin= dict(l=0,r=10,b=10,t=30), yaxis_title=None, xaxis_title=None)
    
    g2.plotly_chart(fig, use_container_width=True) 
    