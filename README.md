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
```
SECRET_KEY=your_secret_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Rodando a aplicação
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```
Acesso em http://127.0.0.1:8000

## Logging
- Configuração: `logging.yaml`
- Logs em: `<project_root>/logs/app.log`

## Banco de dados
- SQLite: `banco.db` (root do projeto)
- Criar tabelas: `Base.metadata.create_all(bind=engine)` em `app/db/models.py`

---

## Endpoints

### **Auth**

#### POST /auth/criar_conta
Cria novo usuário.

**Request:**
```json
{
  "nome": "João Silva",
  "email": "joao@example.com",
  "senha": "senha_segura_123",
  "ativo": true,
  "admin": false
}
```

**Response 201:**
```json
{
  "message": "Usuário criado com sucesso",
  "id": 1,
  "email": "joao@example.com"
}
```

**Errors:**
- 400: Usuário já existe
- 422: Dados inválidos (validação Pydantic)
- 500: Erro interno

---

#### POST /auth/login
Autentica usuário e retorna JWT token.

**Request:**
```json
{
  "email": "joao@example.com",
  "senha": "senha_segura_123"
}
```

**Response 200:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- 401: Credenciais inválidas
- 404: Usuário não encontrado
- 500: Erro interno

---

#### GET /auth/users
Lista todos os usuários (requer autenticação).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response 200:**
```json
[
  {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@example.com",
    "ativo": true,
    "admin": false
  }
]
```

**Errors:**
- 401: Não autenticado / token inválido
- 500: Erro interno

---

### **Orders**

#### GET /orders?status={status}
Lista pedidos. Parâmetro `status` opcional: `PENDENTE | CANCELADO | FINALIZADO`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response 200:**
```json
[
  {
    "id": 1,
    "status": "CANCELADO",
    "id_usuario": 1,
    "preco": 25.50
  },
  {
    "id": 2,
    "status": "PENDENTE",
    "id_usuario": 1,
    "preco": 45.00
  }
]
```

**Errors:**
- 401: Não autenticado
- 422: Status inválido
- 500: Erro interno

---

#### POST /orders
Cria novo pedido para o usuário autenticado.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "id_usuario": 1
}
```

**Response 201:**
```json
{
  "message": "Create order: 5",
  "order": {
    "id": 5,
    "status": "PENDENTE",
    "id_usuario": 1,
    "preco": null
  }
}
```

**Errors:**
- 401: Não autenticado
- 422: Dados inválidos
- 500: Erro interno

---

#### POST /orders/cancel/{order_id}
Cancela um pedido (apenas admin ou dono do pedido).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "message": "Order 1 canceled successfully",
  "order": {
    "id": 1,
    "status": "CANCELADO",
    "price": 25.50
  }
}
```

**Errors:**
- 401: Não autorizado / não é admin nem dono
- 404: Pedido não encontrado
- 500: Erro interno

---

#### POST /orders/{order_id}/add_item
Adiciona item a um pedido.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "produto": "Pizza Margherita",
  "quantidade": 2,
  "preco_unitario": 25.00
}
```

**Response 201:**
```json
{
  "message": "Item adicionado com sucesso",
  "item": {
    "id": 1,
    "pedido_id": 1,
    "produto": "Pizza Margherita",
    "quantidade": 2,
    "preco_unitario": 25.00,
    "subtotal": 50.00
  }
}
```

**Errors:**
- 401: Não autenticado
- 404: Pedido não encontrado
- 422: Dados inválidos
- 500: Erro interno

---

## Erros Padronizados

### ErrorResponse
```json
{
  "detail": "Descrição do erro"
}
```

### Validation Error (422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Autenticação

- Tipo: OAuth2 Password Bearer
- Token URL: `/auth/login-form`
- Formato Header: `Authorization: Bearer <token>`
- Token válido por: `ACCESS_TOKEN_EXPIRE_MINUTES` (padrão 30 min)

---

## Troubleshooting

| Erro | Causa | Solução |
|------|-------|---------|
| `SECRET_KEY não está definida` | .env ausente ou incompleto | Crie `app/.env` com SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES |
| `Logs vazios` | pasta `logs/` não existe | Execute `mkdir logs` ou deixe a config criar automaticamente |
| `401 Unauthorized` | Token expirado ou inválido | Faça novo login em `/auth/login` |
| `404 Not Found` | Recurso não existe | Confirme IDs de usuário/pedido existem |
| `422 Validation Error` | Dados inválidos | Valide tipos e campos obrigatórios |

---

## Referências
- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Passlib: https://passlib.readthedocs.io
- JWT (PyJWT): https://pyjwt.readthedocs.io