"""Acesso a dados de categorias e produtos."""
from sqlalchemy.orm import Session

from app.models.categoria import Categoria
from app.models.produto import Produto


# ----- Categoria -----
def criar_categoria(db: Session, categoria: Categoria) -> Categoria:
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def listar_categorias(db: Session) -> list[Categoria]:
    return db.query(Categoria).all()


def buscar_categoria(db: Session, categoria_id: int) -> Categoria | None:
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


# ----- Produto -----
def criar_produto(db: Session, produto: Produto) -> Produto:
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def buscar_produto(db: Session, produto_id: int) -> Produto | None:
    return db.query(Produto).filter(Produto.id == produto_id).first()


def listar_produtos(db: Session, categoria: str | None = None, busca: str | None = None) -> list[Produto]:
    query = db.query(Produto)
    if categoria:
        query = query.join(Categoria).filter(Categoria.nome.ilike(f"%{categoria}%"))
    if busca:
        query = query.filter(Produto.nome.ilike(f"%{busca}%"))
    return query.all()
