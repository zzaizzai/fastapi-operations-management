from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from db import db_manager, fetch_all_as_dict
from .model import ProductControl
router = APIRouter(prefix="/products")

templates = Jinja2Templates(directory=["app/core/templates", "app/products/templates"])


@router.get("/index")
async def products_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/detail/{product_id}")
async def product_detail(request: Request, product_id: int):
    context = {}
    context['request'] = request
    
    product_control = ProductControl(product_id=product_id)
    product_control.find_a_product_with_id()
    product_control.find_child_parts()
    
    parts = product_control.get_child_parts()
    
    if product_control.exist_product() is False:
        return RedirectResponse("/products/index")

    context['product'] = product_control.get_a_product()
    context['parts'] = parts
    
    return templates.TemplateResponse("product_model_detail.html", context)

@router.get("/search")
async def search_products_model(request: Request, q: str = None):
    html = "search_products_model.html"
    
    context = {}
    context['request'] = request
    context['q'] = q
    
    if q is None or len(q) == 0:
        context['q'] = ''
        return templates.TemplateResponse(html, context)
    
    pc = ProductControl(q=q)
    pc.search_products_with_q()
    
    if pc.exist_product() is False :
        context['msg'] = "No result"
        return templates.TemplateResponse(html, context)

    context['products'] = pc.get_products()
    
    return templates.TemplateResponse(html, context)



@router.get("/api/get_all")
async def api_get_all_products_model():
    
    return ProductControl().get_all()
