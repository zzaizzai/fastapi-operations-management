from fastapi import APIRouter, HTTPException
from db import db_manager, fetch_all_as_dict

router = APIRouter()

@router.get("/items")
async def create_item():
    cursor = db_manager.get_cursor()
    cursor.execute('select * from products')
    
    items = fetch_all_as_dict(cursor)
    cursor.close()
    
    return items
