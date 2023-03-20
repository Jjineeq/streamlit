import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

##############
# 모듈화 필요 #
##########################################################################################
os.chdir("C:\\Users\\99kit\\Desktop\\CapstoneDesign_SmartFactory\\NASA_Bearing\\2nd_test")  #ChangeDirectory 작업경로변경
file_list=glob.glob("**/*.39", recursive=True)                                              #해당폴더및하위폴더에서'.39'로끝나는모든파일찾기
##########################################################################################

# 페이지 기본 설정
st.set_page_config(page_icon="🫠",
                   page_title="CBMforSmartFactory-SignalProcessing",
                   layout="wide")
plt.rcParams['font.family']="NanumGothic"

# 페이지 헤더, 서브 헤더 제목 설정
st.header("Signal Processing(신호 처리)")

# RMS
def rms(stat):                                                    #RootMeanSquare 신호의제곱값평균의제곱근
    return(np.sqrt(np.mean(stat**2, axis=0)))                     #axis=0 sqrt(각변수의모든행의제곱값에대한평균)
rms_arr=np.array([])
for file in file_list:
    df=pd.read_csv(file, sep='\t', header=None)
    rms_value=rms(df.values)                                        #4행*1열
    rms_arr=np.concatenate([rms_arr, rms_value], axis=0)            #반복문통해결국4*984행*1열,즉3936행*1열
rms_arr=rms_arr.reshape(len(file_list), 4)                          #984행*4열
rms_df=pd.DataFrame(rms_arr, columns=['Ch 1', 'Ch 2', 'Ch 3', 'Ch 4'])
rms_df.to_csv("C:/Users/99kit/Desktop/CapstoneDesign_SmartFactory/"
              "NASA_Bearing\\2nd_test/RMS_Bearing.csv", index=None) #984행*4열

# 페이지 컬럼 분할
col1, col2 = st.columns([1, 2])

col1.subheader("RMS(Root Mean Square)")
col1.write("시간 경과에 따른 신호의 평균 전력을 계산하는 기술로써 AC 신호의 전력을 특성화하는 데 유용합니다.")
col1.write("1개 파일 내 20,480개 값을 단일 값으로 표현한 뒤, 984개의 단일 값을 연속적으로 나타냈습니다.")

col2.line_chart(rms_df)