"""Acesso a dados de pedidos e pagamentos."""
from sqlalchemy.orm import Session

from app.models.pagamento import Pagamento
from app.models.pedido import Pedido


def criar_pedido(db: Session, pedido: Pedido) -> Pedido:
    db.add(pedido)
    db.commit()
    db.refresh(pedido)
    return pedido


def salvar(db: Session, pedido: Pedido) -> Pedido:
    db.commit()
    db.refresh(pedido)
    return pedido


def buscar_pedido(db: Session, pedido_id: int) -> Pedido | None:
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()


def listar_por_usuario(db: Session, usuario_id: int) -> list[Pedido]:
    return db.query(Pedido).filter(Pedido.usuario_id == usuario_id).all()


def criar_pagamento(db: Session, pagamento: Pagamento) -> Pagamento:
    db.add(pagamento)
    db.commit()
    db.refresh(pagamento)
    return pagamento
