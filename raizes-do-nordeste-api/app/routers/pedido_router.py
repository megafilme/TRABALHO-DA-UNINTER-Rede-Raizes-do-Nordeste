"""Rotas de pedidos."""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.pedido import AtualizarStatusRequest, PedidoCriar, PedidoResposta
from app.services import auth_service, pedido_service

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResposta, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    dados: PedidoCriar,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(auth_service.get_current_user),
):
    """Cria um pedido para o usuario logado (status inicial PENDENTE)."""
    return pedido_service.criar_pedido(db, usuario.id, dados)


@router.get("", response_model=List[PedidoResposta])
def listar_meus_pedidos(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(auth_service.get_current_user),
):
    """Lista os pedidos do usuario logado."""
    return pedido_service.listar_meus_pedidos(db, usuario.id)


@router.get("/{pedido_id}", response_model=PedidoResposta)
def consultar_pedido(
    pedido_id: int,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(auth_service.get_current_user),
):
    """Consulta um pedido especifico."""
    return pedido_service.obter_pedido(db, pedido_id, usuario)


@router.patch(
    "/{pedido_id}/status",
    response_model=PedidoResposta,
    dependencies=[Depends(auth_service.get_current_admin)],
)
def atualizar_status(
    pedido_id: int,
    dados: AtualizarStatusRequest,
    db: Session = Depends(get_db),
):
    """Atualiza o status do pedido (somente administrador)."""
    return pedido_service.atualizar_status(db, pedido_id, dados.novo_status)
