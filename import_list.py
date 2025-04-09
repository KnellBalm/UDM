## 경고 제거##
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

## DataFrame & visual option ##
import pandas as pd
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_columns', None) 
import polars as pl

import numpy as np
import os
import json

## geo ##
import geopandas as gpd

## Visualize option ##
import seaborn as sns
import matplotlib.pyplot as plt
import ipywidgets as widgets

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'D2Coding'
