import sqlite3
import json
from typing import List, Dict, Any


DATABASE_URL = 'database.db'


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_URL)
        self.conn.row_factory = sqlite3.Row  # row_factory 설정
    
    def get_cursor(self):
        return self.conn.cursor()
    
    def close(self):
        self.conn.close()

# 데이터베이스 매니저 인스턴스 생성
db_manager = DatabaseManager()

# 데이터베이스 커넥션 닫기 위한 함수
def close_database_connection() -> None:
    db_manager.close()

# 딕셔너리 형태로 결과 가져오는 함수
def fetch_all_as_dict(cursor) -> List[Dict[str, Any]]:
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    results = []
    
    for row in rows:
        row_dict = dict(zip(columns, row))
        for key, value in row_dict.items():
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
                try:
                    row_dict[key] = json.loads(value)
                except json.JSONDecodeError:
                    pass
        results.append(row_dict)

    return results