class UnsupportedDBTypeError(Exception):
    """지원하지 않는 DB 타입 예외"""
    def __init__(self, db_type):
        super().__init__(f"Unsupported DB type: {db_type}")
