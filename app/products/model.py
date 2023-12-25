from db import db_manager, fetch_all_as_dict
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, get_type_hints, Type


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

class ProductControl():

    product_data: List[Dict[str, Any]] = []
    parts: List[Dict[str, Any]] = []
    
    exist_parts: bool = False
    
    def __init__(self, product_id: int = None, name: str = None, q: str = None):
        self.product_id = product_id
        self.name = name
        self.q = q
    
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
    