import json
import logging
from pathlib import Path

def load_config(config_path: str = None):
    """config.json 로드"""
    if not config_path:
        default_path = Path(__file__).parent / "config.json"
        config_path = str(default_path)
    if not Path(config_path).exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_logger(name="DBConnector", log_file="db_connector.log"):
    """로깅 설정 (파일 + 콘솔 출력)"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

        # 파일 로깅
        fh = logging.FileHandler(Path(__file__).parent / log_file, encoding="utf-8")
        fh.setFormatter(fmt)
        logger.addHandler(fh)

        # 콘솔 로깅
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(sh)

    return logger
