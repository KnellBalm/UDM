#####################################example#######################################################
# python3 Edit_dbconn_config.py db_conn_config.json target_db_name ip port database user password #
###################################################################################################
import json
import argparse
import os

def add_or_update_database(config_file, db_key, host, port, dbname, user, password):
    try:
        # config 파일이 비어 있거나 없으면 기본 구조를 생성
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                try:
                    config_data = json.load(f)
                except json.JSONDecodeError:
                    # JSON 형식이 깨졌거나 비어있을 때 기본 구조 설정
                    config_data = {"databases": {}}
        else:
            config_data = {"databases": {}}
        
        # DB가 이미 존재하는지 확인하고, 존재하면 업데이트
        if db_key in config_data['databases']:
            print(f"Database '{db_key}' exists. Updating the configuration.")
        else:
            print(f"Database '{db_key}' does not exist. Adding new configuration.")

        # DB 설정을 업데이트하거나 새로 추가
        config_data['databases'][db_key] = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "passwd": password
        }

        # 업데이트된 config 파일을 다시 저장
        with open(config_file, 'w') as f:
            json.dump(config_data, f, indent=4)
        
        print(f"Database '{db_key}' successfully added/updated in {config_file}")
    
    except Exception as e:
        print(f"Error updating config file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Add or update a database configuration in the config.json file.")
    
    # 명령줄 인자 정의
    parser.add_argument('config_file', type=str, help='Path to the config file (e.g., config.json)')
    parser.add_argument('db_key', type=str, help='Database key (e.g., db1, db2)')
    parser.add_argument('host', type=str, help='Database host (e.g., localhost)')
    parser.add_argument('port', type=str, help='Database port (e.g., 5432)')
    parser.add_argument('dbname', type=str, help='Database name (e.g., mydb)')
    parser.add_argument('user', type=str, help='Database user (e.g., myuser)')
    parser.add_argument('password', type=str, help='Database password (e.g., mypassword)')
    
    # 명령줄 인자 파싱
    args = parser.parse_args()

    # 인자로 받은 값으로 데이터베이스 추가 또는 업데이트
    add_or_update_database(
        config_file=args.config_file,
        db_key=args.db_key,
        host=args.host,
        port=args.port,
        dbname=args.dbname,
        user=args.user,
        password=args.password
    )

if __name__ == '__main__':
    main()