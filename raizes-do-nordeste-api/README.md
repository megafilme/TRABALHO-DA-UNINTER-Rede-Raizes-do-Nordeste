# Rede Raízes do Nordeste — API (Back-End)

API REST de e-commerce de produtos regionais do Nordeste, desenvolvida em **Python / FastAPI** como Projeto de Desenvolvimento Back-End da UNINTER.

**Acadêmico:** Marcos Vinícius Vieira dos Santos Junior — **RU:** 4760301

---

## Tecnologias

- **Python 3.11+**
- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **SQLite** (padrão, sem configuração) ou **PostgreSQL**
- **JWT (PyJWT)** — autenticação
- **bcrypt** — hash de senhas

## Arquitetura em camadas

```
routers/        -> recebe as requisições HTTP (camada de apresentação)
services/       -> regras de negócio (camada de negócio)
repositories/   -> acesso ao banco (camada de dados)
models/         -> entidades mapeadas para tabelas
schemas/        -> validação de entrada/saída (Pydantic)
core/           -> configuração e segurança
```

## Como rodar

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/raizes-do-nordeste-api.git
cd raizes-do-nordeste-api

# 2. Criar e ativar um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. (Opcional) configurar variáveis de ambiente
cp .env.example .env

# 5. Popular o banco com dados de exemplo
python seed.py

# 6. Subir a aplicação
uvicorn app.main:app --reload
```

A API ficará disponível em **http://127.0.0.1:8000**
A documentação interativa (Swagger) fica em **http://127.0.0.1:8000/docs**

## Usuários criados pelo seed

| Perfil  | E-mail            | Senha     |
|---------|-------------------|-----------|
| Admin   | admin@raizes.com  | admin123  |
| Cliente | ana@email.com     | ana12345  |

## Endpoints principais

| Método | Rota                     | Descrição                       | Acesso   |
|--------|--------------------------|---------------------------------|----------|
| POST   | /auth/register           | Cadastra um cliente             | Público  |
| POST   | /auth/login              | Autentica e retorna o token JWT | Público  |
| GET    | /produtos                | Lista produtos (filtro/busca)   | Público  |
| GET    | /produtos/{id}           | Detalha um produto              | Público  |
| POST   | /produtos                | Cadastra um produto             | Admin    |
| POST   | /pedidos                 | Cria um pedido                  | Cliente  |
| GET    | /pedidos                 | Lista os pedidos do usuário     | Cliente  |
| GET    | /pedidos/{id}            | Consulta um pedido              | Cliente  |
| POST   | /pagamentos              | Processa pagamento (mock)       | Cliente  |
| PATCH  | /pedidos/{id}/status     | Atualiza o status do pedido     | Admin    |

> Rotas protegidas exigem o cabeçalho `Authorization: Bearer <token>`.

## Fluxo crítico: Pedido → Pagamento Mock → Status

1. Cliente autentica (`POST /auth/login`) e recebe o token JWT.
2. Cria o pedido (`POST /pedidos`) — o sistema valida o estoque, calcula o total e grava com status **PENDENTE**.
3. Solicita o pagamento (`POST /pagamentos`) — o **gateway mock** decide o resultado.
4. Se **aprovado**: status vira **PAGO** e o estoque é baixado.
   Se **recusado**: status vira **CANCELADO** (retorna HTTP 402).
5. O administrador avança o status: **PAGO → ENVIADO → ENTREGUE** (`PATCH /pedidos/{id}/status`).

### Regra do gateway mock

- `cartao`: aprovado, exceto se o número terminar em **0**;
- `pix` e `boleto`: sempre aprovados.

### Máquina de estados

```
PENDENTE --(aprovado)--> PAGO --> ENVIADO --> ENTREGUE
   |
   +--(recusado/cancelado)--> CANCELADO
```

## Exemplo rápido (cURL)

```bash
# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"ana@email.com","senha":"ana12345"}' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# Criar pedido
curl -X POST http://127.0.0.1:8000/pedidos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"itens":[{"produto_id":1,"quantidade":2}]}'

# Pagar
curl -X POST http://127.0.0.1:8000/pagamentos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pedido_id":1,"metodo":"cartao","numero_cartao":"4111111111111111"}'
```

## Estrutura de pastas

```
raizes-do-nordeste-api/
├── app/
│   ├── core/          # config + segurança (JWT, hash)
│   ├── models/        # tabelas (SQLAlchemy)
│   ├── schemas/       # validação (Pydantic)
│   ├── repositories/  # acesso a dados
│   ├── services/      # regras de negócio
│   ├── routers/       # endpoints
│   ├── database.py    # conexão e sessão
│   └── main.py        # aplicação FastAPI
├── seed.py            # dados iniciais
├── requirements.txt
├── .env.example
└── .gitignore
```

---

Projeto acadêmico — UNINTER, 2026.
