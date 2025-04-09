# 1. 라이브러리 

#경고 표시
import warnings 
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# 통계
import statistics 


#데이터 다루기
import numpy as np
import pandas as pd
import sympy as sp

#그림그리기
import matplotlib.pyplot as plt
import seaborn as sns

#선형모델
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor


#

#회귀계수 줄이기
from sklearn.linear_model import ElasticNet, Lasso, Ridge


# 조합
from itertools import combinations

# import booster

import scipy as sc
import sympy as sy
import math as m


#2. 함수

# heatmap corr그림 그리는 함수

def prettyCorr(x, width=15, height=7):
  plt.figure(figsize=(width, height))
  mask = np.zeros_like(x.corr(), dtype= np.bool)
  mask[np.triu_indices_from(mask)] = True
  sns.heatmap(x.corr(), annot=True, fmt='.2f', mask=mask, cmap='YlOrBr')
  plt.show()


#RMSLE
def rmsle(x, y_true, y_hat):
  return np.sqrt( np.mean((np.log(y_hat + 1) - np.log(y_true + 1)) ** 2))

#Linear Regression Coefficient score

def coef(coefs, x):
  tmp = []
  for coef in coefs:
    tmp.append('{:0.02f}'.format(coef))

  if isinstance(x, np.ndarray):
    x = pd.DataFrame(x)
  coef_ = pd.DataFrame( tmp, columns=['coef'] )
  col = pd.DataFrame( x.columns, columns=['columns'] )
  return pd.concat( [coef_, col], axis=1)

#Adjusted R2(R2값, 독립변수, 종속변수)
def adjustedR2(R2,x,y):
  return 1 - ( 1 - R2 ) * (len(y) - 1 ) / (len(y) - x.shape[1] - 1)

# checksubset
def checkSubset(x, y, columns):
  model = LinearRegression().fit(x[columns], y)
  score = model.score(x[columns], y)
  ret = adjustedR2(score, x[columns], y)
  return {'model': model, 'adjR2': ret, 'columns': columns}

# Scikit-learn - SequentialFeatureSelector
from sklearn.feature_selection import SequentialFeatureSelector

#전진선택법
def forward(x, y):
  
  selected_columns = []
  
  for i in range(0, x.shape[1]):
    forward_columns = [col for col in x.columns if col not in selected_columns]
    result = []
    
    for col in forward_columns:
      ret = checkSubset(x, y, selected_columns + [col])
      result.append(ret)

    # 정확도가 가장 높은 조합을 찾아야 합니다. 
    models = pd.DataFrame(result)
    best_model = models.loc[ models.adjR2.argmax()] #model에서 adjR2 점수가 가장 좋았던(argmax)
    if i: 
      if best_model.adjR2 > before_model.adjR2: before_model = best_model
      else: break
    else:
      before_model = best_model     #before model이 처음에 없기 때문에 best model이 before model이 될 수 있도록 함
    selected_columns = best_model.columns
    
  return before_model

#후진소거법


def backward(x, y):
  selected_columns = list(x.columns)

  for i in range(0, x.shape[1]):
    result = []
    for combo in combinations(selected_columns, len(selected_columns) - 1):
      ret = checkSubset(x, y, list(combo))
      result.append(ret)
    
    models = pd.DataFrame(result)
    best_model = models.loc[ models.adjR2.argmax()]
    if i:
      if best_model.adjR2 > before_model.adjR2: before_model = best_model
      else: break
    else:
      before_model = best_model 
    selected_columns = best_model.columns
  return before_model

# 전진+후진 선택법

def forward_select(x, y, selected_columns):
  forward_columns = [col for col in x.columns if col not in selected_columns]
  result = []
  
  for col in forward_columns:
    ret = checkSubset(x, y, selected_columns + [col])
    result.append(ret)
  
  models = pd.DataFrame(result)
  best_model = models.loc[ models.adjR2.argmax()]
  return best_model

def backward_drop(x, y, selected_columns):
  result = []

  for combo in combinations(selected_columns, len(selected_columns) - 1):
    ret = checkSubset(x, y, list(combo))
    result.append(ret)

  models = pd.DataFrame(result)
  best_model = models.loc[ models.adjR2.argmax()]
  return best_model

def step_wise(x, y):
  selected_columns = []
  
  for i in range(0, x.shape[1]):
    forward_model = forward_select(x, y, selected_columns)
    selected_columns = forward_model.columns
  
    if i < 2: before_model = forward_model; continue

    backward_model = backward_drop(x, y, selected_columns)

    large_model = forward_model
    if forward_model.adjR2 < backward_model.adjR2:
      selected_columns = backward_model.columns
      large_model = backward_model

    if large_model.adjR2 > before_model.adjR2: before_model = large_model
    else: break
  
  return before_model