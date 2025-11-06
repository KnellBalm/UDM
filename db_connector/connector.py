import json
from sqlalchemy import create_engine, text
import pandas as pd
from pathlib import Path
from .exceptions import UnsupportedDBTypeError
from .utils import load_config, get_logger


class DBConnector:
    """
    범용 데이터베이스 커넥터 클래스

    ✅ 지원 DBMS:
        - PostgreSQL
        - MySQL

    ✅ 주요 기능:
        - config.json 또는 dict로 연결정보 불러오기
        - SQLAlchemy 엔진 자동 생성
        - 커넥션 풀 기반 연결 재사용
        - 쿼리 실행 결과를 pandas DataFrame으로 반환
        - 실행 내역 로깅 (파일 저장)

    ✅ 사용 예시 (Jupyter Notebook)
        >>> from db_connector.connector import DBConnector
        >>> db = DBConnector(config_path='/mnt/d/project/db_connector/config.json')
        >>> df = db.run_query("SELECT * FROM users LIMIT 5;")
        >>> display(df)

        >>> db.run_query(
        ...     "UPDATE users SET active=1 WHERE id=:id",
        ...     {"id": 3},
        ...     as_df=False
        ... )

    """

    _engine_cache = {}  # ✅ connection 재사용 캐시

    def __init__(self, config: dict = None, config_path: str = None, connection_name: str = None, echo: bool = False):
        """
        Args:
            config (dict): Python dict 형태의 DB 설정
            config_path (str): JSON 설정파일 경로
            connection_name (str): 연결명 (config['default'] 사용)
            echo (bool): SQLAlchemy 로그 출력 여부
        """
        self.config = config or load_config(config_path)
        self.connection_name = connection_name or self.config.get("default")
        self.logger = get_logger("DBConnector")
        self.engine = self._get_or_create_engine(echo)

    def _get_or_create_engine(self, echo=False):
        """Connection 재사용 엔진 생성"""
        if self.connection_name in DBConnector._engine_cache:
            self.logger.info(f"Using cached engine for '{self.connection_name}'")
            return DBConnector._engine_cache[self.connection_name]

        conn_info = self.config["connections"][self.connection_name]
        db_type = conn_info["db_type"].lower()

        url_map = {
            "postgresql": "postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}",
            "mysql": "mysql+pymysql://{username}:{password}@{host}:{port}/{database}",
        }

        if db_type not in url_map:
            raise UnsupportedDBTypeError(db_type)

        db_url = url_map[db_type].format(**conn_info)
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=5,             # ✅ 커넥션 풀 사이즈
            max_overflow=3,          # ✅ 초과 연결 허용
            echo=echo
        )

        DBConnector._engine_cache[self.connection_name] = engine
        self.logger.info(f"Created new engine for '{self.connection_name}'")
        return engine

    def run_query(self, query: str, params: dict = None, as_df: bool = True):
        """SQL 쿼리를 실행하고 결과를 반환합니다."""
        self.logger.info(f"Running query on '{self.connection_name}': {query[:80]}...")
        with self.engine.connect() as conn:
            result = conn.execute(text(query), params or {})
            if query.strip().lower().startswith("select"):
                df = pd.DataFrame(result.fetchall(), columns=result.keys()) if as_df else result.fetchall()
                self.logger.info(f"Query returned {len(df)} rows.")
                return df
            else:
                conn.commit()
                rowcount = result.rowcount
                self.logger.info(f"Query affected {rowcount} rows.")
                return rowcount

    def get_engine(self):
        """SQLAlchemy 엔진 객체 반환"""
        return self.engine
