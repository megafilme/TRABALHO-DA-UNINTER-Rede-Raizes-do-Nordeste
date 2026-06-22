"""Popula o banco com dados iniciais para facilitar os testes.

Uso:
    python seed.py
"""
from app.core.security import gerar_hash_senha
from app.database import Base, SessionLocal, engine
from app import models  # noqa: F401
from app.models.categoria import Categoria
from app.models.produto import Produto
from app.models.usuario import Usuario

Base.metadata.create_all(bind=engine)


def popular():
    db = SessionLocal()
    try:
        if db.query(Usuario).first():
            print("O banco ja possui dados. Nada foi feito.")
            return

        # Usuarios
        admin = Usuario(
            nome="Administrador",
            email="admin@raizes.com",
            senha_hash=gerar_hash_senha("admin123"),
            perfil="admin",
        )
        cliente = Usuario(
            nome="Ana Cliente",
            email="ana@email.com",
            senha_hash=gerar_hash_senha("ana12345"),
            perfil="cliente",
        )
        db.add_all([admin, cliente])
        db.commit()

        # Categorias
        temperos = Categoria(nome="temperos")
        artesanato = Categoria(nome="artesanato")
        alimentos = Categoria(nome="alimentos")
        db.add_all([temperos, artesanato, alimentos])
        db.commit()

        # Produtos
        produtos = [
            Produto(nome="Pimenta-de-cheiro 100g", descricao="Pimenta tipica do Nordeste",
                    preco=12.50, estoque=40, categoria_id=temperos.id),
            Produto(nome="Rapadura artesanal 500g", descricao="Doce de cana puro",
                    preco=13.00, estoque=25, categoria_id=alimentos.id),
            Produto(nome="Renda renascenca (toalha)", descricao="Artesanato pernambucano",
                    preco=89.90, estoque=10, categoria_id=artesanato.id),
            Produto(nome="Cuscuz de milho 1kg", descricao="Farinha de milho flocada",
                    preco=8.75, estoque=60, categoria_id=alimentos.id),
        ]
        db.add_all(produtos)
        db.commit()

        print("Banco populado com sucesso!")
        print("  Admin   -> admin@raizes.com / admin123")
        print("  Cliente -> ana@email.com   / ana12345")
    finally:
        db.close()


if __name__ == "__main__":
    popular()
