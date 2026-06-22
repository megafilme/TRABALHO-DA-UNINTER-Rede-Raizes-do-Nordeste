"""Modelo da tabela 'usuarios'."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False, default="cliente")  # 'cliente' ou 'admin'
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pedidos = relationship("Pedido", back_populates="usuario")
