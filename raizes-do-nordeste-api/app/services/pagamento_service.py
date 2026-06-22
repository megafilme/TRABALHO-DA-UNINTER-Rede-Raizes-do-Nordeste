"""Regras de negocio de pagamento, incluindo o gateway simulado (mock)."""
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.pagamento import Pagamento, StatusPagamento
from app.models.pedido import StatusPedido
from app.repositories import pedido_repo, produto_repo
from app.schemas.pagamento import PagamentoCriar


def _gateway_mock(metodo: str, numero_cartao: str | None) -> bool:
    """Gateway simulado.

    Regra deterministica (facil de testar):
      - cartao: aprovado, exceto se o numero terminar em '0';
      - pix / boleto: sempre aprovado.
    """
    if metodo == "cartao":
        if not numero_cartao:
            return False
        return not numero_cartao.strip().endswith("0")
    return metodo in ("pix", "boleto")


def processar_pagamento(db: Session, usuario, dados: PagamentoCriar) -> Pagamento:
    pedido = pedido_repo.buscar_pedido(db, dados.pedido_id)
    if pedido is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido nao encontrado.")
    if usuario.perfil != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Voce nao tem acesso a este pedido.")
    if pedido.status != StatusPedido.PENDENTE:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Pedido nao esta pendente (status atual: {pedido.status}).",
        )

    aprovado = _gateway_mock(dados.metodo, dados.numero_cartao)

    pagamento = Pagamento(
        pedido_id=pedido.id,
        metodo=dados.metodo,
        status=StatusPagamento.APROVADO if aprovado else StatusPagamento.RECUSADO,
        transacao_id=f"MOCK-{uuid.uuid4().hex[:6].upper()}" if aprovado else None,
    )

    if aprovado:
        # Baixa definitiva de estoque.
        for item in pedido.itens:
            produto = produto_repo.buscar_produto(db, item.produto_id)
            produto.estoque -= item.quantidade
        pedido.status = StatusPedido.PAGO
    else:
        pedido.status = StatusPedido.CANCELADO

    pedido.atualizado_em = datetime.now(timezone.utc)
    pedido_repo.criar_pagamento(db, pagamento)
    pedido_repo.salvar(db, pedido)

    if not aprovado:
        # Pagamento recusado -> informa o cliente com 402.
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED,
            "Pagamento recusado. O pedido foi cancelado.",
        )

    return pagamento
