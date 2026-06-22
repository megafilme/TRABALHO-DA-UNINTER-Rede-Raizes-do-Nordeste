"""Configuracoes da aplicacao, lidas de variaveis de ambiente (ou de valores padrao)."""
import os


def _carregar_env() -> None:
    """Le um arquivo .env simples (chave=valor), se existir, sem dependencias extras."""
    caminho = os.path.join(os.getcwd(), ".env")
    if not os.path.exists(caminho):
        return
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha or linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            os.environ.setdefault(chave.strip(), valor.strip())


_carregar_env()


class Settings:
    """Reune as configuracoes usadas no projeto."""

    PROJECT_NAME: str = "Rede Raizes do Nordeste - API"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./raizes.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "chave-secreta-de-desenvolvimento")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


settings = Settings()
