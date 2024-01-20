from fastapi import APIRouter

from .enpoints_operation import router as product_router_1
from .api import router as product_router_api

router = APIRouter()

router.include_router(product_router_1, prefix="/products")
router.include_router(product_router_api, prefix="/products/api")