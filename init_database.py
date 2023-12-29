import sqlite3
import random
from datetime import datetime, timedelta


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
    
    cursor.execute('''
        DROP TABLE IF EXISTS parts_model;
    ''')
    
    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE products_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location_produce TEXT DEFAULT "Factory1" ,
            location_sell TEXT DEFAULT "Nagoya" ,
            customer TEXT DEFAULT "Toyota",
            price_sell INTEGER,
            lead_time INTEGER --days
        );
    ''')

    # 새로운 테이블 생성
    cursor.execute('''
        CREATE TABLE products_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER,
            lot INTEGER,
            datetime_created DATETIME DEFAULT CURRENT_TIMESTAMP,
            datetime_produced DATETIME, 
            date_due DATE,
            datetime_sold DATETIME, 
            location_current TEXT DEFAULT "Factory1" ,
            process TEXT DEFAULT "waiting start" 
            
        );
    ''')

    cursor.execute('''
        CREATE TABLE parts_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            parent_product_id INTEGER,
            location_produce TEXT DEFAULT "Factory1" ,
            price_produce INTEGER
            
        );
    ''')

    # 변경 사항 저장
    db.commit()
    cursor.close()
    # 데이터베이스 연결 닫기
    
def get_random_string_part() -> str:
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"  # 0부터 9까지의 숫자
    
    random_word = ''.join(random.choice(characters) for _ in range(5))
    
    # 랜덤한 숫자 부분 생성 (예: 00325)
    random_numbers = ''.join(random.choice(numbers) for _ in range(5)) 
    
    # 문자열과 숫자를 연결하여 반환
    result = random_word + '-' + random_numbers
    return result

def get_random_string_product() -> str:
    characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "0123456789"  # 0부터 9까지의 숫자
    
    random_word = ''.join(random.choice(characters) for _ in range(5))
    
    # 랜덤한 숫자 부분 생성 (예: 00325)
    random_numbers = ''.join(random.choice(numbers) for _ in range(5))  
    # 랜덤한 숫자 부분 생성 (예: 00325)
    random_numbers_second = ''.join(random.choice(numbers) for _ in range(3))  
    # 문자열과 숫자를 연결하여 반환
    result = random_word + '-' + random_numbers + '-' + random_numbers_second
    return result



def add_part(name, parent_product_id):
    cursor = db.cursor()
    random_price = random.randint(50, 500)
    cursor.execute("""
                INSERT INTO parts_model 
                (name, parent_product_id, price_produce) 
                VALUES (?, ?, ?)
                """, 
                (name, parent_product_id, random_price))
    db.commit()
    cursor.close()
    
    
def add_product(name):
    cursor = db.cursor()
    random_lead_time = random.randint(2, 12)
    random_price = random.randint(5000, 10000)
    cursor.execute("""
                INSERT INTO products_model 
                (name, price_sell, lead_time) 
                VALUES (?, ?, ?)
                """, 
                (name,random_price, random_lead_time))
    db.commit()    
    cursor.close()


def add_product_history(product_id):
    cursor = db.cursor()
    today = datetime.today()
    random_days = random.randint(7, 14)
    random_date = today + timedelta(days=random_days)
    sql_formatted_date = random_date.strftime('%Y-%m-%d')

    random_quantity = random.randint(20, 50)
    cursor.execute('INSERT INTO products_history (product_id, quantity, date_due) VALUES (?, ?, ?)', 
                (product_id, random_quantity, sql_formatted_date))
    db.commit()    
    cursor.close()

def create_demodata() -> None:
    initialize_database()
    num_data = 200
    
    for _ in range(1, num_data):
        add_product(get_random_string_product())

    for i in range(1, num_data):
        add_part(get_random_string_part(), i)
        add_part(get_random_string_part(), i)
        add_part(get_random_string_part(), i)
        add_part(get_random_string_part(), i)
        add_part(get_random_string_part(), i)
    
    #create operations
    for _ in range(1,300):
        random_product_id = random.randint(1, num_data - 1 )
        add_product_history(random_product_id)
    
    print("Database initialized and tables created.")
    
if __name__ == "__main__":
    create_demodata()
    