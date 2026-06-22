"""Regras de autenticacao e autorizacao."""
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.database import get_db
from app.models.usuario import Usuario
from app.repositories import usuario_repo
from app.schemas.usuario import UsuarioCriar

# Esquema de seguranca: o token chega no cabecalho "Authorization: Bearer <token>".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def registrar(db: Session, dados: UsuarioCriar, perfil: str = "cliente") -> Usuario:
    if usuario_repo.buscar_por_email(db, dados.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Ja existe um usuario com este e-mail.")
    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=security.gerar_hash_senha(dados.senha),
        perfil=perfil,
    )
    return usuario_repo.criar(db, usuario)


def autenticar(db: Session, email: str, senha: str) -> str:
    usuario = usuario_repo.buscar_por_email(db, email)
    if not usuario or not security.verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "E-mail ou senha invalidos.")
    return security.criar_token_acesso({"sub": str(usuario.id), "perfil": usuario.perfil})


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Usuario:
    """Dependencia: valida o token e devolve o usuario logado."""
    credenciais_invalidas = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Token invalido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = security.decodificar_token(token)
        usuario_id = payload.get("sub")
        if usuario_id is None:
            raise credenciais_invalidas
    except jwt.PyJWTError:
        raise credenciais_invalidas

    usuario = usuario_repo.buscar_por_id(db, int(usuario_id))
    if usuario is None:
        raise credenciais_invalidas
    return usuario


def get_current_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    """Dependencia: garante que o usuario logado e administrador."""
    if usuario.perfil != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acesso restrito a administradores.")
    return usuario
