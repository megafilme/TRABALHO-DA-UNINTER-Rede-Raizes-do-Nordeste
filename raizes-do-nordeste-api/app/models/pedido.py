"""Modelo da tabela 'pedidos' e os possiveis status."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class StatusPedido:
    """Status possiveis de um pedido (maquina de estados do fluxo critico)."""

    PENDENTE = "PENDENTE"
    PAGO = "PAGO"
    ENVIADO = "ENVIADO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"


# Transicoes permitidas: de qual status pode ir para quais status.
TRANSICOES_VALIDAS = {
    StatusPedido.PENDENTE: {StatusPedido.PAGO, StatusPedido.CANCELADO},
    StatusPedido.PAGO: {StatusPedido.ENVIADO, StatusPedido.CANCELADO},
    StatusPedido.ENVIADO: {StatusPedido.ENTREGUE},
    StatusPedido.ENTREGUE: set(),
    StatusPedido.CANCELADO: set(),
}


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    status = Column(String(20), nullable=False, default=StatusPedido.PENDENTE)
    valor_total = Column(Numeric(10, 2), nullable=False, default=0)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    atualizado_em = Column(DateTime, nullable=True)

    usuario = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
    pagamento = relationship("Pagamento", back_populates="pedido", uselist=False)
