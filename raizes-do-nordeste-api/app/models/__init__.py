"""Importa todos os modelos para que o SQLAlchemy os registre ao criar as tabelas."""
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.pedido import Pedido, StatusPedido
from app.models.item_pedido import ItemPedido
from app.models.pagamento import Pagamento, StatusPagamento

__all__ = [
    "Usuario",
    "Categoria",
    "Produto",
    "Pedido",
    "StatusPedido",
    "ItemPedido",
    "Pagamento",
    "StatusPagamento",
]
