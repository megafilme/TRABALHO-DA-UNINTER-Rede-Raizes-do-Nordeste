"""Schemas (Pydantic) de categoria e produto."""
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ----- Categoria -----
class CategoriaCriar(BaseModel):
    nome: str = Field(..., min_length=2, max_length=80)


class CategoriaResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str


# ----- Produto -----
class ProdutoCriar(BaseModel):
    nome: str = Field(..., min_length=2, max_length=160)
    descricao: Optional[str] = None
    preco: Decimal = Field(..., ge=0)
    estoque: int = Field(..., ge=0)
    categoria_id: Optional[int] = None


class ProdutoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: Optional[str]
    preco: Decimal
    estoque: int
    categoria_id: Optional[int]
