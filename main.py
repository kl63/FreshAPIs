from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import inspect


# Import database modules
from database.database import engine, get_db, Base
from core.config import settings as app_settings

# Import models to register them with SQLAlchemy
import models.product  # This registers the Product model with SQLAlchemy
import models.user    # This registers the User model with SQLAlchemy
import models.category  # This registers the Category model with SQLAlchemy
import models.order   # This registers the Order model with SQLAlchemy
import models.setting # This registers the Setting model with SQLAlchemy
import models.language # This registers the Language model with SQLAlchemy
import models.coupon   # This registers the Coupon model with SQLAlchemy

# Import routers
from routers import products, auth, categories, orders, languages, attributes, settings as settings_router, coupons

# Create FastAPI app with settings from config
app = FastAPI(
    title=app_settings.APP_NAME,
    description=app_settings.APP_DESCRIPTION,
    version=app_settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from the Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables on startup
@app.on_event("startup")
async def startup_db_client():
    # Create tables only if they don't already exist
    # This ensures we don't lose data during restarts
    # The 'checkfirst=True' parameter makes sure tables are not recreated if they exist
    if not app_settings.TESTING:  # Don't create tables in test mode
        Base.metadata.create_all(bind=engine, checkfirst=True)

# Include routers
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(settings_router.router)
app.include_router(languages.router)
app.include_router(attributes.router)
app.include_router(coupons.router)

@app.get(
    "/",
    summary="Welcome Page",  # This becomes the "title" in Swagger
    description="This is the root endpoint of the Freshly API. It provides a welcome message and basic info.",
    tags=["General"]
)
async def root():
    return {
        "message": "Welcome to Freshly Supermarket API",
        "documentation": "/docs",
        "version": app_settings.APP_VERSION
    }
@app.get("/health")
def health_check():
    return {"status": "ok"}
