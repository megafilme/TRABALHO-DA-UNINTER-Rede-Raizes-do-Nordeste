"""Rotas de autenticacao: cadastro e login."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.schemas.usuario import LoginRequest, TokenResposta, UsuarioCriar, UsuarioResposta
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticacao"])


@router.post("/register", response_model=UsuarioResposta, status_code=status.HTTP_201_CREATED)
def registrar(dados: UsuarioCriar, db: Session = Depends(get_db)):
    """Cadastra um novo cliente."""
    return auth_service.registrar(db, dados)


@router.post("/login", response_model=TokenResposta)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    """Autentica o usuario e retorna um token JWT."""
    token = auth_service.autenticar(db, dados.email, dados.senha)
    return TokenResposta(
        access_token=token,
        token_type="bearer",
        expira_em=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
