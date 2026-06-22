"""Regras de negocio de pedidos (fluxo critico)."""
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.item_pedido import ItemPedido
from app.models.pedido import Pedido, StatusPedido, TRANSICOES_VALIDAS
from app.repositories import pedido_repo, produto_repo
from app.schemas.pedido import PedidoCriar


def criar_pedido(db: Session, usuario_id: int, dados: PedidoCriar) -> Pedido:
    """Cria o pedido (status PENDENTE), validando estoque e calculando o total."""
    pedido = Pedido(usuario_id=usuario_id, status=StatusPedido.PENDENTE, valor_total=Decimal("0"))
    total = Decimal("0")

    for item in dados.itens:
        produto = produto_repo.buscar_produto(db, item.produto_id)
        if produto is None:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Produto {item.produto_id} nao encontrado."
            )
        if produto.estoque < item.quantidade:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"Estoque insuficiente para o produto '{produto.nome}'.",
            )
        pedido.itens.append(
            ItemPedido(
                produto_id=produto.id,
                quantidade=item.quantidade,
                preco_unitario=produto.preco,
            )
        )
        total += produto.preco * item.quantidade

    pedido.valor_total = total
    return pedido_repo.criar_pedido(db, pedido)


def listar_meus_pedidos(db: Session, usuario_id: int):
    return pedido_repo.listar_por_usuario(db, usuario_id)


def obter_pedido(db: Session, pedido_id: int, usuario, somente_admin_ve_tudo: bool = True) -> Pedido:
    pedido = pedido_repo.buscar_pedido(db, pedido_id)
    if pedido is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido nao encontrado.")
    # Cliente so pode ver os proprios pedidos; admin ve qualquer um.
    if usuario.perfil != "admin" and pedido.usuario_id != usuario.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Voce nao tem acesso a este pedido.")
    return pedido


def atualizar_status(db: Session, pedido_id: int, novo_status: str) -> Pedido:
    pedido = pedido_repo.buscar_pedido(db, pedido_id)
    if pedido is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pedido nao encontrado.")

    novo_status = novo_status.upper()
    permitidos = TRANSICOES_VALIDAS.get(pedido.status, set())
    if novo_status not in permitidos:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Transicao invalida: de '{pedido.status}' para '{novo_status}'.",
        )

    pedido.status = novo_status
    pedido.atualizado_em = datetime.now(timezone.utc)
    return pedido_repo.salvar(db, pedido)
