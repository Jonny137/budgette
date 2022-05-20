from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteException

from core.config import settings
from routers.expense import expense_router
from routers.expense_type import exp_type_router
from error_handling.exceptions import (
    BudgetteException, budgette_exception_handler, generic_error_handler)
from core.log_config import LOG_CONFIG

dictConfig(LOG_CONFIG)

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_STR}/openapi.json'
)

# CORS setup
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin
                       in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

# Attach API routes
app.include_router(exp_type_router, prefix=settings.API_STR + '/expense_type')
app.include_router(expense_router, prefix=settings.API_STR + '/expense')

# Add error handlers
app.add_exception_handler(Exception, generic_error_handler)
app.add_exception_handler(BudgetteException, budgette_exception_handler)
app.add_exception_handler(StarletteException, budgette_exception_handler)
