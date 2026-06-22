"""Rotas de categorias e produtos."""
from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.produto import (
    CategoriaCriar,
    CategoriaResposta,
    ProdutoCriar,
    ProdutoResposta,
)
from app.services import auth_service, produto_service

router = APIRouter(tags=["Produtos"])


# ----- Categorias -----
@router.get("/categorias", response_model=List[CategoriaResposta])
def listar_categorias(db: Session = Depends(get_db)):
    return produto_service.listar_categorias(db)


@router.post(
    "/categorias",
    response_model=CategoriaResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_service.get_current_admin)],
)
def criar_categoria(dados: CategoriaCriar, db: Session = Depends(get_db)):
    return produto_service.criar_categoria(db, dados)


# ----- Produtos -----
@router.get("/produtos", response_model=List[ProdutoResposta])
def listar_produtos(
    categoria: Optional[str] = None,
    busca: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """Lista produtos, com filtro opcional por categoria e busca por nome."""
    return produto_service.listar_produtos(db, categoria, busca)


@router.get("/produtos/{produto_id}", response_model=ProdutoResposta)
def detalhar_produto(produto_id: int, db: Session = Depends(get_db)):
    return produto_service.obter_produto(db, produto_id)


@router.post(
    "/produtos",
    response_model=ProdutoResposta,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_service.get_current_admin)],
)
def criar_produto(dados: ProdutoCriar, db: Session = Depends(get_db)):
    """Cadastra um produto (somente administrador)."""
    return produto_service.criar_produto(db, dados)
