"""Schemas (Pydantic) de pagamento."""
from typing import Optional

from pydantic import BaseModel, Field


class PagamentoCriar(BaseModel):
    pedido_id: int
    metodo: str = Field(..., examples=["cartao"])  # cartao / pix / boleto
    numero_cartao: Optional[str] = Field(None, examples=["4111111111111111"])


class PagamentoResposta(BaseModel):
    pedido_id: int
    status_pagamento: str
    status_pedido: str
    transacao_id: Optional[str]
