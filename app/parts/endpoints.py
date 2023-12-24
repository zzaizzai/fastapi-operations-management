from fastapi import APIRouter, Request
from db import db_manager, fetch_all_as_dict
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/parts")

templates = Jinja2Templates(directory=["app/core/templates", "app/parts/templates"])

@router.get("/index")
async def parts_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/api/search")
async def api_search_parts_model(q: str = None):
    if q is None:
        return "no data"
    
    cursor = db_manager.get_cursor()
    cursor.execute(f"""
        SELECT 
            *,
            (SELECT json_object(
                'id', id, 
                'name', name
                ) FROM products_model WHERE id = parts_model.parent_product_id) AS parent_product
        FROM 
            parts_model
        WHERE 
            parts_model.name LIKE '%{q}%'
        """)
        
    
    items = fetch_all_as_dict(cursor)
    cursor.close()
    
    return items



@router.get("/api/get_all")
async def api_get_all_parts_model():
    cursor = db_manager.get_cursor()
    cursor.execute("""
            select 
            *,
            (SELECT json_object(
                'id', id, 
                'name', name
                ) FROM products_model WHERE id = parts_model.parent_product_id) AS parent_product
            from 
                parts_model
                """)
    
    items = fetch_all_as_dict(cursor)
    cursor.close()
    
    return items

