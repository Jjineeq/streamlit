import streamlit as st
import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

##############
# 모듈화 필요 #
################
# 데이타 불러오기
rms_df=pd.read_csv("C:/Users/99kit/Desktop/CapstoneDesign_SmartFactory/"
                   "NASA_Bearing/2nd_test/RMS_Bearing.csv")
TrD=rms_df.values[0:400, :]                                                             #400행*4열
TsD=rms_df.values                                                                       #984행*4열
TrScore_arr=np.zeros([TrD.shape[0], TrD.shape[1]])                                      #np.zeros((400,4)) 1600개의0으로구성
TsScore_arr=np.zeros([TsD.shape[0], TrD.shape[1]])                                      #np.zeros((984,4)) 3936개의0으로구성

#MSET
lr=LinearRegression()
input_idx=np.arange(TrD.shape[1]).tolist()                                              #np.arange(4).tolist() [0,1,2,3]
for idx in input_idx:                                                                   #0
    input_idx=np.arange(TrD.shape[1]).tolist()                                          #[0,1,2,3]
    input_idx.remove(idx)                                                               #[1,2,3]
    lr.fit(TrD[:, input_idx], TrD[:, idx])                                              #x=TrD[:,[1,2,3]],y=TrD[:,0] 훈련데이터에서하나의변수를나머지변수셋의선형결합으로학습.즉,가중치및절편학습
    TrScore_arr[:, idx]=lr.predict(TrD[:, input_idx])                                   #훈련데이터의세변수가주어졌을때y에대한예측값 변수당400개의예측값
    TsScore_arr[:, idx]=lr.predict(TsD[:, input_idx])                                   #변수당984개의예측값
TsScore_arr=pd.DataFrame(TsScore_arr, columns=['p_Ch 1', 'p_Ch 2', 'p_Ch 3', 'p_Ch 4'])

def bootlimit(stat, bootstrap, SigLev):                                         #bootstrap은원본데이터로부터B회의복원추출을통해B개의데이터셋을얻는방법
    ConLev=100-SigLev*100                                                       #ConfidentialLevel=100-SignificanceLevel 신뢰수준
    smplsz=len(stat)
    smpld_lmt=[]
    for i in range(bootstrap):
        smpld_lmt.append(np.percentile(np.random.choice(stat, smplsz), ConLev)) #stat에서smplsz개의샘플을복원추출,해당데이터의ConLev분위수추출
    lmt=np.mean(smpld_lmt)                                                      #bootstrap개데이터의평균
    return(lmt)

# Degradation Model
l2norm_TrScore=np.sqrt(np.sum(TrScore_arr**2, axis=1))      #norm=벡터의크기=벡터의길이=벡터의시작점과끝점거리=두데이터의유사도를나타내는척도
                                                            #L2Norm=EuclideanDistance 가장짧은직선거리
TrDegScore=np.cumsum(l2norm_TrScore)/np.arange(1, 401, 1)   
l2norm_TsScore=np.sqrt(np.sum(TsScore_arr**2, axis=1))
TsDegScore=np.cumsum(l2norm_TsScore)/np.arange(1, 985, 1)
cl_2=bootlimit(TrDegScore, SigLev=0.05, bootstrap=100)

yval2=np.full((984,), cl_2)
cmplx2=np.concatenate([TsDegScore, yval2], axis=0)
cmplx2=cmplx2.reshape(2, 984)
cmplx2=np.transpose(cmplx2)
##########################################

# 페이지 기본 설정
st.set_page_config(page_icon="🫠",
                   page_title="CBMforSmartFactory-RULPrediction",
                   layout="wide")
plt.rcParams['font.family']="NanumGothic"

# 페이지 헤더, 서브 헤더 제목 설정
st.header("RUL Prediction(잔여 수명 예측)")

# 페이지 컬럼 분할
col1, col2 = st.columns([1, 2])

col1.write("모델을 이용하여 잔여 수명을 예측합니다.")
col1.write("이때, 시계열성을 반영하도록 가중치를 부여합니다.")

# exponential weight
def exponential_weight(length, alpha):
    exp_weight = []
    for i in range(1, length+1):
        w = alpha * (1-alpha)**i
        exp_weight.append(w)
    exp_weight = sorted(exp_weight, reverse=False)
    return(exp_weight)

# Exponentially Weighted Linear Regression
t=900
w=exponential_weight(length=t, alpha=0.05)

x=np.arange(t)
x=x.reshape(t, 1)
y=TsDegScore[0:t].values.reshape(t, 1)

EWLR = LinearRegression(fit_intercept=True)
EWLR.fit(x,y, sample_weight = w)

coef = EWLR.coef_
intercept = EWLR.intercept_

# predefined failure threshold
failure_threshold = max(TsDegScore)

# RUL Prediction Visualization
cl = bootlimit(TrDegScore, SigLev=0.05, bootstrap=100)

fig, ax = plt.subplots()

ax.plot(TsDegScore, color='blue', label='Test Data')
ax.set_xlim([0, 1200])
ax.set_ylim([min(TsDegScore), max(TsDegScore)*1.005])


x = np.arange(1400)
linear_curve = coef * x[:900] + intercept
linear_curve = np.concatenate([np.zeros(500), linear_curve])  # add zeros to match length of x
ax.plot(x, linear_curve, color='darkcyan', label='Exponentially Weighted Linear Regression')


# x = np.arange(1400)
# linear_curve = coef*x + intercept
# ax.plot(linear_curve[0], color='darkcyan', label='Exponentially Weighted Linear Regression')

ax.axhline(y=failure_threshold, color='red', label='Failure Threshold')
ax.axhline(y=cl, color='green', label='Confidence Limit')

ax.legend()

st.pyplot(fig)

# # Visualization of RUL Prediction
# cl = bootlimit(TrDegScore, SigLev=0.05, bootstrap=100)

# plt.plot(TsDegScore)

# plt.xlim([0, 1200])
# plt.ylim([min(TsDegScore), max(TsDegScore)*1.005])

# x = np.arange(1400)
# linear_curve = coef*x + intercept
# plt.plot(linear_curve[0], color='darkcyan')


###########################################
# Create a Matplotlib plot
fig, ax = plt.subplots()
ax.plot(x, y)

ax.axhline(y=failure_threshold, color='red')
ax.axhline(y=cl, color='red')

# Display the plot in Streamlit
st.pyplot(fig)
###########################################

# Result of RUL Prediction
predicted_failureTime= int((failure_threshold-intercept) / coef) # coef가 a라고 보면 됨필기한거있지
RUL = predicted_failureTime-t

# print('예측 잔여시점: %2.2f시점' % RUL)
# print('예측 잔여수명: %2.4f일' % (RUL*10/60/24))
# print()
# print('실제 잔여시점: %2.2f시점' % (984-t))
# print('실제 잔여수명: %2.4f일' % ((984-t)*10/60/24))