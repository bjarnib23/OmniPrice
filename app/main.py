from fastapi import FastAPI
from app.api import stores, products, price_logs
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="OmniPrice",
    description="Automated Market Intelligence & Price Analytics Engine",
    version="0.1.0",
)

app.include_router(stores.router, prefix="/api/stores", tags=["stores"])
app.include_router(products.router, prefix="/api/products", tags=["products"])
app.include_router(price_logs.router, prefix="/api/price-logs", tags=["price-logs"])


@app.get("/")
def root():
    return {"status": "ok", "message": "OmniPrice API is running"}
