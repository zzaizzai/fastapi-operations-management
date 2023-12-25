from db import db_manager, fetch_all_as_dict

from typing import Dict, Any, List


class ProductControl():

    product_data: List[Dict[str, Any]] = []
    
    def __init__(self, product_id: int = None, name: str = None, q: str = None):
        self.product_id = product_id
        self.name = name
        self.q = q
    
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
    