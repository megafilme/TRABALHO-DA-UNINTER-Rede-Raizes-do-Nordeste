"""Rotas de pagamento."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.pagamento import PagamentoCriar, PagamentoResposta
from app.services import auth_service, pagamento_service

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("", response_model=PagamentoResposta)
def processar_pagamento(
    dados: PagamentoCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(auth_service.get_current_user),
):
    """Processa o pagamento de um pedido usando o gateway simulado (mock)."""
    pagamento = pagamento_service.processar_pagamento(db, usuario, dados)
    return PagamentoResposta(
        pedido_id=pagamento.pedido_id,
        status_pagamento=pagamento.status,
        status_pedido=pagamento.pedido.status,
        transacao_id=pagamento.transacao_id,
    )
