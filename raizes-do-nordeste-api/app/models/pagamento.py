"""Modelo da tabela 'pagamentos' e os possiveis status."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class StatusPagamento:
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"


class Pagamento(Base):
    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False, unique=True)
    metodo = Column(String(20), nullable=False)  # cartao / pix / boleto
    status = Column(String(20), nullable=False)
    transacao_id = Column(String(40), nullable=True)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pedido = relationship("Pedido", back_populates="pagamento")
