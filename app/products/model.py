from datetime import datetime, timedelta, date
from typing import Dict, Any, List, get_type_hints, Type, Optional
from operator import itemgetter

from db import db_manager, fetch_all_as_dict



class Product():
    def __init__(self, 
                product_id: int = None, 
                name: str = None, 
                location_produce: str = None,
                customer: str = None,
                price_sell: float = None):
        
        self.product_id = product_id
        self.name = name
        self.location_produce = location_produce
        self.customer = customer
        self.price_sell = price_sell


class ProductOperation():
    
    operations_data: List[Dict[str, Any]] = []
    operation_detail_data: Dict[str, Any] = {}
    
    def __init__(self, 
                product_id: Optional[int] = None, 
                q: Optional[str] = None, 
                sort: str = 'asc', 
                order: Optional[str] = None,
                operation_id: Optional[int]  = None
                ):
        self.product_id = product_id
        self.q = q
        self.sort = sort
        self.order = order
        self.operation_id = operation_id
    
    def get_product_operation_detail(self):
        if len(self.operation_detail_data) == 0:
            self._get_product_operation_detail()
        return self.operation_detail_data
    
    @staticmethod
    def calculate_business_days(start_date: datetime, days_to_subtract: int) -> datetime:
        current_date = start_date
        while days_to_subtract > 0:
            current_date -= timedelta(days=1)
            if current_date.weekday() < 5:  # Monday to Friday are considered business days (0 to 4)
                days_to_subtract -= 1
        return current_date
    
    def get_time_line(self)-> List[Dict[str, Any]]:
        if len(self.operation_detail_data) == 0:
            return []
        
        time_line_list = []
        today = date.today().strftime('%Y-%m-%d')
        
        time_line_list.append({"title": "Today","date": today})
        time_line_list.append({"title": "Created","date":self.operation_detail_data['datetime_created']})
        # time_line_list.append({"title": 'datetime_sold',"date":self.operation_detail_data['datetime_sold']})
        time_line_list.append({"title": 'Due',"date":self.operation_detail_data['date_due']})
        time_line_list.append({"title": 'Start Plan Calculated',"date":self.get_date_start_plan_calculated()})

        # 날짜를 기준으로 리스트 정렬
        sorted_time_line = sorted(time_line_list,  key=itemgetter('date'))
        return sorted_time_line
    
    def get_date_start_plan_calculated(self) -> str:
        if len(self.operation_detail_data) == 0:
            return 'none'
        
        data = self.operation_detail_data
        date_due = datetime.strptime(data['date_due'], '%Y-%m-%d')

        # Calculate the new date by subtracting business days
        new_date = self.calculate_business_days(date_due, data['lead_time'])

        # Format the new date as a string in the desired format
        new_date_str = new_date.strftime('%Y-%m-%d')


        # Format the new date as a string in the desired format
        new_date_str = new_date.strftime('%Y-%m-%d')
        
        return new_date_str
    
    
    def _get_product_operation_detail(self) -> None:
        self.operation_detail_data

        cursor = db_manager.get_cursor()
        query = f"""
            SELECT 
                ph.*, 
                pm.name AS product_name ,
                pm.lead_time AS lead_time 
            FROM products_operation ph 
            LEFT JOIN products_model pm ON ph.product_id = pm.id
            WHERE ph.id = {self.operation_id}
            """
            
        cursor.execute(query)
        operation_detail = fetch_all_as_dict(cursor)
        cursor.close()
        if len(operation_detail) > 0:
            self.operation_detail_data= operation_detail[0]
    
    def search_products_operation_with_id(self, product_id: int) -> Type['ProductOperation']:
        
        cursor = db_manager.get_cursor()
        query = f"""
            SELECT 
                ph.*, 
                pm.name AS product_name 
            FROM products_operation ph 
            LEFT JOIN products_model pm ON ph.product_id = pm.id
            WHERE ph.product_id = '{product_id}'
            """
        cursor.execute(query)
        products = fetch_all_as_dict(cursor)
        self.operations_data = products
        cursor.close()
        
        return self
        
    def search_products_with_q(self) -> None:
        
        # # get all
        # if self.q is None or len(self.q) == 0:
        #     self.operation_data = self.get_all()
        #     return
        
        cursor = db_manager.get_cursor()
        query = """
            SELECT 
                ph.*, 
                pm.name AS product_name 
            FROM products_operation ph 
            LEFT JOIN products_model pm ON ph.product_id = pm.id
            """
    
        if self.q:
            query += f"WHERE pm.name LIKE '%{self.q}%'"
        
        if self.order:
            query += f"ORDER BY {self.order} {self.sort} "
    
        cursor.execute(query)
        products = fetch_all_as_dict(cursor)
        cursor.close()
        
        self.operations_data = products
    
    def get_operations_data(self) -> List[Dict[str, Any]]:
        if len(self.operations_data) == 0:
            self.search_products_with_q()
        return self.operations_data
    
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        cursor = db_manager.get_cursor()
        cursor.execute("""
                    select 
                        ph.*, 
                        pm.name as product_name 
                    from products_operation ph 
                    left join products_model pm on ph.product_id = pm.id
                    """)
        items = fetch_all_as_dict(cursor)
        cursor.close()
        return items
    
class ProductControl():

    product_data: List[Dict[str, Any]] = []
    parts: List[Dict[str, Any]] = []
    
    exist_parts: bool = False
    
    def __init__(self, 
                product_id: Optional[int] = None, 
                name: Optional[str] = None, 
                q: Optional[str] = None):
        self.product_id = product_id
        self.name = name
        self.q = q
    
    def add_price_produce(self) -> None:
        self.product_data[0]['price_produce'] = self.calculate_price_produce()
        
    def calculate_price_produce(self) -> float:
        price_total = 0
        
        if self.parts == []:
            return price_total
        
        for i, item in enumerate(self.parts):
            price_total += item['price_produce'] or 0
        
        return price_total
    
    @classmethod
    def get_all(cls) -> List[Dict[str, Any]]:
        cursor = db_manager.get_cursor()
        cursor.execute('select * from products_model')
        items = fetch_all_as_dict(cursor)
        cursor.close()
        return items
    
    def get_child_parts(self) -> List[Dict[str, Any]]:
        return self.parts
    
    def exist_parts(self) -> bool:
        return len(self.parts) > 1
    
    def find_child_parts(self) -> None:
        cursor = db_manager.get_cursor()
    
        cursor.execute(f"""
            SELECT 
                *
            FROM 
                parts_model
            WHERE 
                parts_model.parent_product_id = '{self.product_id}'
            """)
            
        
        parts = fetch_all_as_dict(cursor)
        cursor.close()
        self.parts = parts
    
    def get_a_product(self) -> Dict[str, Any]:
        return self.product_data[0]
    
    def get_products(self) -> List[Dict[str, Any]]:
        return self.product_data
    
    def find_a_product_with_id(self) -> None:
        
        if self.product_id is None or self.product_id == "":
            return
        
        cursor = db_manager.get_cursor()
        cursor.execute(f"""
            SELECT 
                *
            FROM 
                products_model
            WHERE 
                products_model.id = '{self.product_id}'
            """)
            
        products = fetch_all_as_dict(cursor)
        cursor.close()
        self.product_data = products
        
    def exist_product(self) -> bool:
        return len(self.product_data) >= 1
    
    
    def search_products_with_q(self) -> None:
        
        if self.q is None or len(self.q) == 0:
            return
        
        cursor = db_manager.get_cursor()
        cursor.execute(f"""
            SELECT 
                *
            FROM 
                products_model
            WHERE 
                products_model.name LIKE '%{self.q}%'
            """)
            
        products = fetch_all_as_dict(cursor)
        cursor.close()
        self.product_data = products
    