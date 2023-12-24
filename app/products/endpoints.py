from fastapi import APIRouter, Request
from db import db_manager, fetch_all_as_dict
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/products")

templates = Jinja2Templates(directory=["app/core/templates", "app/products/templates"])


@router.get("/index")
async def products_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/search")
async def search_products_model(request: Request, q: str = None):
    html = "search_products_model.html"
    
    context = {}
    context['request'] = request
    context['q'] = q
    
    if q is None or len(q) == 0:
        context['q'] = ''
        return templates.TemplateResponse(html, context)
    
    cursor = db_manager.get_cursor()
    cursor.execute(f"""
        SELECT 
            *
        FROM 
            products_model
        WHERE 
            products_model.name LIKE '%{q}%'
        """)
        
    
    products = fetch_all_as_dict(cursor)
    print(products)
    cursor.close()

    
    if len(products) == 0 :
        context['msg'] = "No result"
        return templates.TemplateResponse(html, context)

    context['products'] = products
    
    return templates.TemplateResponse(html, context)



@router.get("/api/get_all")
async def api_get_all_products_model():
    cursor = db_manager.get_cursor()
    cursor.execute('select * from products_model')
    
    items = fetch_all_as_dict(cursor)
    cursor.close()
    
    return items
