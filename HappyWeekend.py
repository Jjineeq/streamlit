import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 페이지 기본 설정
st.set_page_config(page_icon="🫠",
                   page_title="CBMforSmartFactory",
                   layout="wide")
plt.rcParams['font.family']="NanumGothic"

# 페이지 헤더, 서브 헤더 제목 설정
st.header("IMS Bearing Data Set No. 2")

# 데이타 불러오기
file_list=glob.glob("jjineeq/streamlit/main/data/**/*.39", recursive=True)                                              #해당폴더및하위폴더에서'.39'로끝나는모든파일찾기
df=pd.read_csv("jjineeq/streamlit/main/data/2004.02.12.10.32.39", header=None, sep='\t')
df.columns=['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4']

# 페이지 컬럼 분할
col1, col2 = st.columns([1, 2])

col1.subheader("Data Structure")
col1.write("Recording Duration: February 12, 2004 10:32:39 to February 19, 2004 06:22:39")
col1.write("No. of Files: 984")
col1.write("No. of Channels: 4")
col1.write("Channel Arrangement: Bearing 1 – Ch 1; Bearing2 – Ch 2; Bearing3 – Ch 3; Bearing 4 – Ch 4.")
col1.write("File Recording Interval: Every 10 minutes")
col1.write("File Format: ASCII")
col1.write("Description: At the end of the test-to-failure experiment, outer race failure occurred in bearing 1.")

col2.subheader("File No. 1: February 12, 2004 10:32:39")
col2.line_chart(df)

# 버튼
if st.button("코드 보기. 다시 닫지 못합니다."):
    code = '''import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 페이지 기본 설정
st.set_page_config(page_icon="🫠",
                   page_title="CBMforSmartFactory",
                   layout="wide")
plt.rcParams['font.family']="NanumGothic"

# 페이지 헤더, 서브 헤더 제목 설정
st.header("IMS Bearing Data")
st.subheader("Set No. 2")

# 데이타 불러오기
os.chdir("C:\\Users\\99kit\\Desktop\\CapstoneDesign_SmartFactory\\NASA_Bearing\\2nd_test")  #ChangeDirectory 작업경로변경
file_list=glob.glob("**/*.39", recursive=True)                                              #해당폴더및하위폴더에서'.39'로끝나는모든파일찾기
df=pd.read_csv("C:\\Users\\99kit\\Desktop\\CapstoneDesign_SmartFactory\\"
               "NASA_Bearing\\2nd_test\\2004.02.12.10.32.39", header=None, sep='\t')
df.columns=['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4']

# 페이지 컬럼 분할
col1, col2 = st.columns([1, 2])

col1.subheader("Data Structure")
col1.write("Recording Duration: February 12, 2004 10:32:39 to February 19, 2004 06:22:39")
col1.write("No. of Files: 984")
col1.write("No. of Channels: 4")
col1.write("Channel Arrangement: Bearing 1 – Ch 1; Bearing2 – Ch 2; Bearing3 – Ch 3; Bearing 4 – Ch 4.")
col1.write("File Recording Interval: Every 10 minutes")
col1.write("File Format: ASCII")
col1.write("Description: At the end of the test-to-failure experiment, outer race failure occurred in bearing 1.")

col2.subheader("File No. 1: February 12, 2004 10:32:39")
col2.line_chart(df)'''
    st.code(code, language='python')