"""Configuracao da conexao com o banco e da sessao do SQLAlchemy."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# O SQLite precisa deste argumento extra para funcionar com o FastAPI.
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base da qual todos os modelos (tabelas) herdam.
Base = declarative_base()


def get_db():
    """Dependencia do FastAPI: abre uma sessao por requisicao e a fecha no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
