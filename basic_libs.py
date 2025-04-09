# 기본 데이터 처리 라이브러리
import pandas as pd
import numpy as np
from tqdm import tqdm
tqdm.pandas()
pd.set_option('display.max_columns', None)

# 로그 및 경고 처리
import logging
import warnings
warnings.filterwarnings('ignore')  # 경고 무시
import os
import sys
sys.path.append('../../../jupyter_WorkingDirectory/UDM/')

import myLib

# 머신러닝 및 데이터 전처리 라이브러리
import statsmodels.api as sm

from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, mean_squared_error, mean_absolute_error, roc_auc_score, r2_score, make_scorer
from category_encoders import TargetEncoder
from factor_analyzer import FactorAnalyzer
import shap


# 머신러닝 알고리즘
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier, XGBRegressor
from sklearn.linear_model import Lasso, Ridge
from lightgbm import LGBMRegressor
# from catboost import CatBoostClassifier  # 사용시 주석 해제

# 데이터 불균형 처리
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline

# 지리 정보 처리 라이브러리
import geopandas as gpd
from shapely.geometry import Point, Polygon, LineString, box

# 시각화 라이브러리
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager as fm, rc

# 한글 폰트 설정
font_path = '/usr/local/src/python3.10/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf/KoPub Dotum Medium.ttf'
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)

# DuckDB 데이터베이스 연결
import duckdb