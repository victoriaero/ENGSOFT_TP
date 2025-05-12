from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routers import auth

from app.database import engine
from app.models import Base
from app.routers import (
    datasets,
    evaluators,
    dataset_attributes,
    dataset_labels,
    samples,
    sample_rows,
    annotations
)

# Lifespan event handler substituindo on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic: criar tabelas, inicializar recursos
    Base.metadata.create_all(bind=engine)
    # Adicione inicializações de cache, conexões externas etc. aqui
    yield
    # Shutdown logic: limpar recursos
    # Adicione encerramento de conexões, flush de caches etc. aqui
    pass

# Inicializa o FastAPI com lifespan
app = FastAPI(
    title="DataLabeler API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configura CORS para permitir chamadas do front-end
origins = [
    "http://localhost:3000",  # ajuste para o domínio do seu front
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui routers
app.include_router(datasets.router, tags=["datasets"])
app.include_router(evaluators.router, tags=["evaluators"])
app.include_router(dataset_attributes.router, tags=["dataset_attributes"])
app.include_router(dataset_labels.router, tags=["dataset_labels"])
app.include_router(samples.router, tags=["samples"])
app.include_router(sample_rows.router, tags=["sample_rows"])
app.include_router(annotations.router, tags=["annotations"])
app.include_router(auth.router, tags=["auth"])

# Health-check
@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}

# Root endpoint
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to DataLabeler API"}

app.mount(
    "/", 
    StaticFiles(directory=Path(__file__).parent.parent / "frontend", html=True),
    name="static"
)
