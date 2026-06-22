"""Schemas (Pydantic) de pedido e seus itens."""
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemPedidoCriar(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)


class PedidoCriar(BaseModel):
    itens: List[ItemPedidoCriar] = Field(..., min_length=1)


class ItemPedidoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    produto_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal


class PedidoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    status: str
    valor_total: Decimal
    criado_em: datetime
    atualizado_em: Optional[datetime]
    itens: List[ItemPedidoResposta]


class AtualizarStatusRequest(BaseModel):
    novo_status: str = Field(..., examples=["ENVIADO"])
