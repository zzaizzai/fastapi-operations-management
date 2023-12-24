from fastapi import APIRouter, Request
from db import db_manager, fetch_all_as_dict
from fastapi.templating import Jinja2Templates
from init_database import create_demodata

router = APIRouter()

templates = Jinja2Templates(directory="app/core/templates")


@router.get("/")
async def mainpage(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@router.get("/api/create/demodata")
async def api_create_demodata():

    create_demodata()    

    return "done"
