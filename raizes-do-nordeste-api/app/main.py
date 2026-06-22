"""Ponto de entrada da aplicacao FastAPI."""
from fastapi import FastAPI

from app.core.config import settings
from app.database import Base, engine
from app import models  # noqa: F401  (importa os modelos para registrar as tabelas)
from app.routers import auth_router, pagamento_router, pedido_router, produto_router

# Cria as tabelas no banco (se ainda nao existirem).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "API de e-commerce de produtos regionais do Nordeste. "
        "Projeto Back-End UNINTER. "
        "Desenvolvido por Marcos Vinícius Vieira dos Santos Junior."
    ),
)

app.include_router(auth_router.router)
app.include_router(produto_router.router)
app.include_router(pedido_router.router)
app.include_router(pagamento_router.router)


@app.get("/", tags=["Status"])
def raiz():
    """Verifica se a API esta no ar."""
    return {"projeto": settings.PROJECT_NAME, "versao": settings.VERSION, "status": "ok"}
