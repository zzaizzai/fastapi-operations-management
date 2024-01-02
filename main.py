# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.parts import endpoints as e_parts
from app.core import endpoints as e_core
from app.products import endpoints as e_products


app = FastAPI()

app.mount("/static", StaticFiles(directory="app/core/static"), name="static")

app.include_router(e_core.router)
app.include_router(e_products.router)
app.include_router(e_parts.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)