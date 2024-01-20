import time

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..model import ProductControl, ProductOperation


router = APIRouter()


@router.get("/get_all_model")
async def api_get_all_products_model():
    
    return ProductControl().get_all()


@router.get("/get_time_line")
async def api_get_date_plan_calculated(operation_id: int = None):
    time.sleep(2)
    ph = ProductOperation(operation_id=operation_id)
    ph.get_product_operation_detail()
    time_line_list = ph.get_time_line()
    return time_line_list


@router.get("/get_all_model")
async def api_get_all_products_model():
    
    return ProductControl().get_all()


@router.get("/operations")
async def api_operations():
    return ProductOperation.get_all()
