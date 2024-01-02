# Operations Management wirh fastapi

![fastapi](https://img.shields.io/badge/fastapi-0.105-green)
![Python](https://img.shields.io/badge/Python-3.9.13-blue)



## Explain
Simple ERM(Enterprise Resources Planning ) System
I think ERP system with microservice could be commercialized.

**OM(Operations Management)**
Orders(from other system) -> Create Production Operations -> Create Part Operations
-> Calculate Production Plans -> Deliver to Customer

## install
```
python -m venv venv
venv\Scripts\activate
(venv)python -m pip install -r .\requirements.txt
```

## database sqlite
```
python init_database.py
```

## start app
```
uvicorn main:app --host 127.0.0.1 --port 8001 --reload
```