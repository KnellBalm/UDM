"""
This module provides functions to process CSV files and convert them to shapefiles.

Functions:
- process_geodata(file_path, geometry_column_name, convert_column_name_dict): 
  Reads a CSV file, processes geometry columns, and converts it into a GeoDataFrame.
  It renames columns to ensure they are under 10 characters for shapefile compatibility.
"""

import pandas as pd
import geopandas as gpd
from shapely import wkt

def process_geodata(file_path, geometry_column_name, convert_column_name_dict, drop_column_name, set_crs):
    """
    CSV 파일을 변환하여 Shapefile 형식으로 변환하는 함수입니다.

    Parameters:
    file_path (str): CSV 파일 경로
    geometry_column_name (str): CSV 파일에서 geometry 열의 이름
    convert_column_name_dict (dict): CSV의 열 이름을 변경할 때 사용할 딕셔너리 (Shapefile의 열 이름은 10자 이하로 해야 합니다)
    drop_column_name(list) : csv 파일에서 geomtery 변환 후 버릴 컬럼 이름 리스트
    set_crs(int) : 설정하고자 하는 좌표계

    Returns:
    GeoDataFrame: 변환된 GeoDataFrame 객체
    """
    df = pd.read_csv(file_path)
    df['geometry'] = df[geometry_column_name].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.rename(columns=convert_column_name_dict, inplace=True)
    gdf.drop(columns=[x for x in df.columns if any(substring in x for substring in drop_column_name)],inplace=True)
    gdf.set_crs(epsg=set_crs,inplace=True)
    return gdf

if __name__ == "__main__":
    print("It only works for importing the module.")
