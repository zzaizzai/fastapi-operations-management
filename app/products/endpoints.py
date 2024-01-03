from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import time
from .model import ProductControl, ProductOperation
router = APIRouter(prefix="/products")

templates = Jinja2Templates(directory=["app/core/templates", "app/products/templates"])


@router.get("/index")
async def products_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/make_orders")
async def make_product_orders(request: Request):
    return templates.TemplateResponse("make_product_orders.html", {"request": request})

# @router.get("/api/get_date_plan_calculated")
# async def api_get_date_plan_calculated(operation_id: int = None):
#     # time.sleep(2)
#     ph = Productoperation(operation_id=operation_id)
#     date_plan_calculated = ph.get_date_start_plan_calculated()
#     return date_plan_calculated


@router.get("/api/get_time_line")
async def api_get_date_plan_calculated(operation_id: int = None):
    time.sleep(2)
    ph = ProductOperation(operation_id=operation_id)
    ph.get_product_operation_detail()
    time_line_list = ph.get_time_line()
    return time_line_list

@router.get("/api/get_past_operations/{product_id}")
async def api_get_past_operations(product_id: int = None):
    time.sleep(1)
    operations = ProductOperation()\
        .search_products_operation_with_id(product_id=product_id)\
        .get_operations_data()
    return operations



@router.get("/operations")
async def view_operations(request: Request, sort: str = 'asc', order: str = None, q: str = ""):
    context = {}
    context['request'] = request
    context['order'] = order
    context['sort'] = sort
    context['q'] = q
    
    ph = ProductOperation(sort=sort, order=order, q=q)
    ph.search_products_with_q()
    operations = ph.get_operations_data()
    context['operations'] = operations
    return templates.TemplateResponse("product_operations.html", context)

@router.get("/operation_detail/{operation_id}")
async def product_operation_detail(request: Request, operation_id: int):
    context = {}
    context['request'] = request
    ph = ProductOperation(operation_id=operation_id)
    operation = ph.get_product_operation_detail()
    context['operation'] = operation
    
    if len(operation) == 0:
        context['msg'] = 'no data'
        
    return templates.TemplateResponse("product_operation_detail.html", context)

@router.get("/api/operations")
async def api_operations():
    return ProductOperation.get_all()



@router.get("/detail/{product_id}")
async def product_detail(request: Request, product_id: int):
    context = {}
    context['request'] = request
    
    product_control = ProductControl(product_id=product_id)
    product_control.find_a_product_with_id()
    product_control.find_child_parts()
    product_control.add_price_produce()
    
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



@router.get("/api/get_all_model")
async def api_get_all_products_model():
    
    return ProductControl().get_all()
