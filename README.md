# 🛵 API de Delivery (Resumo técnico)

API RESTful para gerenciamento de pedidos, usuários e autenticação (JWT). Projeto em FastAPI + SQLAlchemy (SQLite) com logging configurável.

## Índice

- Pré-requisitos
- Setup
- Variáveis de ambiente
- Rodando a aplicação
- Logging
- Banco de dados / Migrações
- Endpoints (descrição, exemplos de request/response)
- Erros e responses padronizados
- Debug / Troubleshooting
- Testes

---

## Pré-requisitos

- Python 3.10+
- Virtualenv (recomendado)
- SQLite (embutido)

## Setup

1. Criar e ativar venv:
   - PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Instalar dependências:
   ```powershell
   python -m pip install -r requirements.txt
   ```

## Variáveis de ambiente (.env)

Arquivo `app/.env` obrigatório com:

- SECRET_KEY (string)
- ALGORITHM (ex: HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES (int, ex: 30)

Exemplo:

```
SECRET_KEY=your_secret_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Rodando a aplicação

Ative o venv e execute:

```powershell
uvicorn app.main:app --reload
```

Ouvirá por padrão em http://127.0.0.1:8000

## Logging

- Configuração em `logging.yaml`.
- Logs gravados em `<project_root>/logs/app.log` — garanta que a pasta `logs/` exista ou será criada automaticamente pela configuração.

## Banco de dados / Migrações

- Banco padrão: `sqlite:///banco.db` no root do projeto.
- Para migrações com Alembic:
  ```bash
  alembic revision --autogenerate -m "mensagem"
  alembic upgrade head
  ```
- Em desenvolvimento, o projeto também pode criar tabelas via `Base.metadata.create_all(bind=engine)` (ver `app/db/models.py`).

## Autenticação

- OAuth2 Password Bearer configurado com tokenUrl: `/auth/login-form`
- Para endpoints protegidos, envie header:
  ```
  Authorization: Bearer <access_token>
  ```

## Endpoints principais

### POST /auth/criar_conta

- Cria usuário.
- Request JSON: { "nome": "...", "email": "...", "senha": "..." [, "ativo": true, "admin": false] }
- Success 201:
  ```json
  {
    "message": "Usuário criado com sucesso",
    "id": 1,
    "email": "user@example.com"
  }
  ```
- Errors: 400 (usuário existe), 422 (validação), 500 (erro interno).

### POST /auth/login

- Autentica e retorna token.
- Request JSON: { "email": "...", "senha": "..." }
- Success 200:
  ```json
  { "access_token": "xxxx", "token_type": "bearer" }
  ```
- Errors: 401 (credenciais), 404 (usuário não encontrado), 500.

### GET /orders?status={status}

- Lista pedidos. `status` opcional: PENDENTE | CANCELADO | FINALIZADO
- Response: lista de OrderResponse
  ```json
  [{ "id": 1, "status": "CANCELADO", "id_usuario": 1, "preco": 25.5 }]
  ```
- Errors: 401 (autenticação), 422 (validação).

### POST /orders

- Cria pedido para um usuário autenticado.
- Request JSON: { "id_usuario": 1 }
- Success 201: `{ "message": "Create order: 1" }`

### POST /orders/cancel/{order_id}

- Cancela pedido (apenas admin ou dono do pedido).
- Erros: 401 (não autorizado), 404 (não encontrado), 500.

## Responses e erros padronizados

- ErrorResponse: `{ "detail": "<mensagem>" }`
- Validation (422): Pydantic padrão (campo -> mensagens)
- Logging: exceções capturadas usam logger.exception(...) para gravar stack trace.

## Troubleshooting (erros comuns)

- passlib/bcrypt: prefira `passlib[pbkdf2_sha256]` se bcrypt causar problemas; limite bcrypt = 72 bytes para senhas.
- SECRET_KEY ou ALGORITHM nulos: verifique `.env` e se `load_dotenv` está apontando para `app/.env`.
- Logs vazios: verifique `logging.yaml` e a existência da pasta `logs/`.

## Testes

- Rodar testes (se existir):
  ```bash
  pytest -q
  ```
- Gerar requirements:
  ```bash
  python -m pip freeze > requirements.txt
  ```

---

## Referências

- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Passlib: https://passlib.readthedocs.io
