import sqlite3

# SQLite 데이터베이스 연결
db = sqlite3.connect('database.db')

# 테이블 초기화 및 스키마 관리 스크립트
def initialize_database():
    cursor = db.cursor()

    # 기존 테이블이 존재한다면 삭제
    cursor.execute('''
        DROP TABLE IF EXISTS products;
    ''')
    
    cursor.execute('''
        DROP TABLE IF EXISTS products_model;
    ''')
    
    cursor.execute('''
        DROP TABLE IF EXISTS products_history;
    ''')
    
    cursor.execute('''
        DROP TABLE IF EXISTS parts;
    ''')
    
    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE products_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location_produce TEXT DEFAULT "factory1" ,
            customer TEXT DEFAULT "toyota",
            price_sell INTEGER
        );
    ''')

    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE products_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            lot INTEGER,
            datetime_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            datetime_produced DATETIME, 
            datetime_due DATETIME,
            datetime_sold DATETIME, 
            location_current TEXT DEFAULT "factory1" 
            
        );
    ''')

    cursor.execute('''
        CREATE TABLE parts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_product_id INTEGER,
            
        );
    ''')

    # 변경 사항 저장
    db.commit()
    
    # 데이터베이스 연결 닫기

def add_part(description):
    cursor = db.cursor()
    cursor.execute('INSERT INTO parts (description) VALUES (?)', (description,))
    db.commit()


def add_product(name):
    cursor = db.cursor()
    cursor.execute('INSERT INTO products_model (name) VALUES (?)', (name,))
    db.commit()    

if __name__ == "__main__":
    initialize_database()
    print("Database initialized and tables created.")
    add_product('AAA')
    add_product('BBB')
    add_product('CCC')
    add_part('AAA')
    add_part('BBB')
    add_part('CCC')
    db.close()