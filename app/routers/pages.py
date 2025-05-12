# app/routers/pages.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.deps import get_db_session
from app import crud

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/datasets")
def list_datasets_page(request: Request, db: Session = Depends(get_db_session)):
    datasets = crud.get_datasets(db, 0, 100)  # buscar datasets do banco
    return templates.TemplateResponse("datasets.html", {
        "request": request,
        "datasets": datasets
    })
