from fastapi import APIRouter, Request
from db import db_manager, fetch_all_as_dict
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/products")

templates = Jinja2Templates(directory=["app/core/templates", "app/products/templates"])


@router.get("/index")
async def products_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/api/get_all")
async def api_get_all_products_model():
    cursor = db_manager.get_cursor()
    cursor.execute('select * from products_model')
    
    items = fetch_all_as_dict(cursor)
    cursor.close()
    
    return items
