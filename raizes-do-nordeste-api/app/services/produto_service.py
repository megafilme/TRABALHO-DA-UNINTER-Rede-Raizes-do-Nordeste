"""Regras de negocio de categorias e produtos."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.models.produto import Produto
from app.repositories import produto_repo
from app.schemas.produto import CategoriaCriar, ProdutoCriar


def criar_categoria(db: Session, dados: CategoriaCriar) -> Categoria:
    return produto_repo.criar_categoria(db, Categoria(nome=dados.nome))


def listar_categorias(db: Session):
    return produto_repo.listar_categorias(db)


def criar_produto(db: Session, dados: ProdutoCriar) -> Produto:
    if dados.categoria_id is not None and not produto_repo.buscar_categoria(db, dados.categoria_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Categoria informada nao existe.")
    produto = Produto(
        nome=dados.nome,
        descricao=dados.descricao,
        preco=dados.preco,
        estoque=dados.estoque,
        categoria_id=dados.categoria_id,
    )
    return produto_repo.criar_produto(db, produto)


def listar_produtos(db: Session, categoria: str | None, busca: str | None):
    return produto_repo.listar_produtos(db, categoria, busca)


def obter_produto(db: Session, produto_id: int) -> Produto:
    produto = produto_repo.buscar_produto(db, produto_id)
    if produto is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Produto nao encontrado.")
    return produto
