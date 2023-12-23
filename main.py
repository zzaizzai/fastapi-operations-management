# main.py
from fastapi import FastAPI
from app.parts import endpoints


app = FastAPI()


app.include_router(endpoints.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)