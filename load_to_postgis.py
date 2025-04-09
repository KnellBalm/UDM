from sqlalchemy import create_engine
import geopandas as gpd

def upload_to_postgis(gdf, db_url, table_name, if_exists="replace"):
    """
    GeoDataFrame을 PostgreSQL 데이터베이스에 업로드하는 함수.
    
    Parameters:
        gdf (GeoDataFrame): 업로드할 GeoDataFrame.
        db_url (str): PostgreSQL 연결 문자열.
            예: "postgresql://user:password@host:port/dbname"
        table_name (str): PostgreSQL에 저장될 테이블 이름.
        if_exists (str): 테이블 존재 시 동작 방식. 다음 중 하나:
            - "replace": 기존 테이블 대체.
            - "append": 기존 테이블에 데이터 추가.
            - "fail": 동일한 이름의 테이블이 존재하면 에러 발생.
    
    Returns:
        None: 
            데이터가 성공적으로 업로드되면 반환값이 없습니다.
            업로드 중 오류가 발생하면 예외가 발생하여 메시지가 출력됩니다.
    
    Example:
        >>> from upload_to_postgis import upload_to_postgis
        >>> import geopandas as gpd
        >>> db_url = "postgresql://user:password@host:port/dbname"
        >>> gdf = gpd.read_file("path_to_your_file.shp")
        >>> upload_to_postgis(gdf, db_url, "final_result", if_exists="replace")
    
    Notes:
        - `if_exists` 옵션:
            - "replace": 기존 테이블 대체.
            - "append": 기존 테이블에 데이터 추가.
            - "fail": 동일한 이름의 테이블이 존재하면 에러 발생.
        - GeoDataFrame의 좌표 참조 시스템(CRS)은 데이터베이스의 공간 데이터 CRS와 일치해야 합니다.
        - 데이터베이스 연결 문자열은 적절한 사용자명, 비밀번호, 호스트, 포트, 데이터베이스 이름을 포함해야 합니다.

    사용법:
        1. PostgreSQL 연결 문자열 생성
           - "postgresql://user:password@host:port/dbname" 형식으로 작성합니다.
           - 예: "postgresql://myuser:mypassword@localhost:5432/mydatabase"
        
        2. GeoDataFrame 준비
           - GeoPandas를 사용해 데이터를 읽어옵니다.
           - 예: gpd.read_file("path_to_file.shp")
        
        3. upload_to_postgis 함수 호출
           - 업로드하려는 데이터, 연결 문자열, 테이블 이름을 인자로 전달합니다.
           - 기본적으로 동일한 이름의 테이블이 존재하면 대체("replace")합니다.
    """
    try:
        # 데이터베이스 엔진 생성
        engine = create_engine(db_url)
        # GeoDataFrame을 PostgreSQL에 업로드
        gdf.to_postgis(name=table_name, con=engine, if_exists=if_exists)
        print(f"데이터가 '{table_name}' 테이블에 성공적으로 업로드되었습니다!")
    except Exception as e:
        print(f"오류 발생: {e}")
