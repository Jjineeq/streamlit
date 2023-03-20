import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 페이지 기본 설정
st.set_page_config(page_icon="🫠",
                   page_title="CBMforSmartFactory-AnomalyDetection",
                   layout="wide")
plt.rcParams['font.family']="NanumGothic"

# 페이지 헤더, 서브 헤더 제목 설정
st.header("Anomaly Detection(이상 감지)")
st.subheader("MSET(Multivariate State Estimation Technique)")
st.write("모델 기반 이상 감지 방법의 한 종류로써 관찰된 데이터를 기반으로 현재 상태를 추정할 수 있습니다.")
st.write("관찰 데이터와 예측 값이 일치하지 않는 경우, 데이터에 이상 값이 있음을 나타낼 수 있습니다.")
st.write("정상 분포 데이터를 활용하여 정상과 이상을 구분하는 Control Limit를 설정합니다.")

# 페이지 컬럼 분할
col1, col2 = st.columns([2, 2])

# 데이타 불러오기
rms_df=pd.read_csv("C:/Users/99kit/Desktop/CapstoneDesign_SmartFactory/"
                   "NASA_Bearing/2nd_test/RMS_Bearing.csv")
TrD=rms_df.values[0:400, :]                                                 #400행*4열
TsD=rms_df.values                                                           #984행*4열
TrScore_arr=np.zeros([TrD.shape[0], TrD.shape[1]])                          #np.zeros((400,4)) 1600개의0으로구성
TsScore_arr=np.zeros([TsD.shape[0], TrD.shape[1]])                          #np.zeros((984,4)) 3936개의0으로구성

#MSET
lr=LinearRegression()
input_idx=np.arange(TrD.shape[1]).tolist()                                  #np.arange(4).tolist() [0,1,2,3]
for idx in input_idx:                                                       #0
    input_idx=np.arange(TrD.shape[1]).tolist()                              #[0,1,2,3]
    input_idx.remove(idx)                                                   #[1,2,3]
    lr.fit(TrD[:, input_idx], TrD[:, idx])                                  #x=TrD[:,[1,2,3]],y=TrD[:,0] 훈련데이터에서하나의변수를나머지변수셋의선형결합으로학습.즉,가중치및절편학습
    TrScore_arr[:, idx]=lr.predict(TrD[:, input_idx])                       #훈련데이터의세변수가주어졌을때y에대한예측값 변수당400개의예측값
    TsScore_arr[:, idx]=lr.predict(TsD[:, input_idx])                       #변수당984개의예측값
TsScore_arr=pd.DataFrame(TsScore_arr, columns=['p_Ch 1', 'p_Ch 2', 'p_Ch 3', 'p_Ch 4'])
col1.line_chart(TsScore_arr)

intergrated_TrScore=np.sqrt(np.sum(TrScore_arr**2, axis=1))                     #훈련데이터400행*4열을400행*1열로만드는과정
intergrated_TsScore=np.sqrt(np.sum(TsScore_arr**2, axis=1))                     #984행*1열
def bootlimit(stat, bootstrap, SigLev):                                         #bootstrap은원본데이터로부터B회의복원추출을통해B개의데이터셋을얻는방법
    ConLev=100-SigLev*100                                                       #ConfidentialLevel=100-SignificanceLevel 신뢰수준
    smplsz=len(stat)
    smpld_lmt=[]
    for i in range(bootstrap):
        smpld_lmt.append(np.percentile(np.random.choice(stat, smplsz), ConLev)) #stat에서smplsz개의샘플을복원추출,해당데이터의ConLev분위수추출
    lmt=np.mean(smpld_lmt)                                                      #bootstrap개데이터의평균
    return(lmt)
cl_1=bootlimit(intergrated_TrScore, bootstrap=100, SigLev=0.05)                 #변형된훈련데이터의400개샘플에대해100번복원추출,95분위수100개의평균
OutIdx=np.where(intergrated_TsScore>cl_1)[0]                                    #이상치추출

# fig, ax = plt.subplots()
# ax.plot(intergrated_TsScore)
# plt.axhline(cl_1, color='red')
# col2.pyplot(fig)

yval=np.full((984,), cl_1)
cmplx=np.concatenate([intergrated_TsScore, yval], axis=0)
cmplx=cmplx.reshape(2, 984)
cmplx=np.transpose(cmplx)
col2.line_chart(cmplx)

if col2.button('이상치'):
    col2.write(OutIdx)