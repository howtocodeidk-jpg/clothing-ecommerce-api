from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.database import Base, SessionLocal, engine
from app.models.role import Role
from app.routes import auth, product, cart, address, order, payment, review, coupons
from app.utils.response import error_response
from fastapi.staticfiles import StaticFiles

# --------------------------------------------------
# Create FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Clothing Ecommerce API",
    version="1.0.0",
    description="Backend API for Clothing Ecommerce with RBAC"
)

# --------------------------------------------------
# CORS Configuration (For React Frontend)
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Create Database Tables
# --------------------------------------------------

Base.metadata.create_all(bind=engine)

# --------------------------------------------------
# Include Routers
# --------------------------------------------------

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(address.router)
app.include_router(order.router)
app.include_router(review.router)
app.include_router(payment.router)
app.include_router(coupons.router)


# --------------------------------------------------
# Global Exception Handler
# --------------------------------------------------

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Database error occurred",
            "data": None,
            "errors": str(exc)
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "data": None,
            "errors": str(exc)
        }
    )

# --------------------------------------------------
# Health Check Route
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "success": True,
        "message": "Clothing Ecommerce API is running 🚀",
        "data": None,
        "errors": None
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.on_event("startup")
def create_roles():
    db = SessionLocal()

    role_data = [
        {"id": 1, "name": "SuperAdmin"},
        {"id": 2, "name": "Admin"},
        {"id": 3, "name": "User"},
    ]

    for role in role_data:
        exists = db.query(Role).filter(Role.id == role["id"]).first()
        if not exists:
            db.add(Role(id=role["id"], name=role["name"]))

    db.commit()
    db.close()
