from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse


homework_router = APIRouter(tags=["Homeworks"])