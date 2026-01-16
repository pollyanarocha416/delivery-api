# 🛵 API de Delivery

API para gerenciamento de pedidos, usuários e autenticação (JWT). Projeto em FastAPI + SQLAlchemy (SQLite) com logging configurável.

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Setup](#setup)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Rodando a Aplicação](#rodando-a-aplicação)
- [Autenticação](#autenticação)
- [Pedidos](#pedidos)
- [Troubleshooting](#troubleshooting)
- [Referências](#referências)

---

## Pré-requisitos

- Python 3.8+
- pip ou conda
- SQLite3 (incluído no Python)

---

## Setup

1. **Clone o repositório**:

```bash
git clone https://github.com/pollyanarocha416/delivery-api.git
cd delivery-api
```

2. **Crie um ambiente virtual**:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente** (criar arquivo `app/.env`):

```env
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

5. **Execute as migrações do banco de dados**:

```bash
alembic upgrade head
```

---

## Variáveis de Ambiente

Crie um arquivo `app/.env` na raiz do projeto com as seguintes variáveis:

| Variável                      | Descrição                                        | Exemplo                       |
| ----------------------------- | ------------------------------------------------ | ----------------------------- |
| `SECRET_KEY`                  | Chave secreta para assinar tokens JWT            | `sua_chave_super_secreta_123` |
| `ALGORITHM`                   | Algoritmo de criptografia JWT                    | `HS256`                       |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token de acesso em minutos | `30`                          |

**⚠️ Nota de Segurança**: Nunca compartilhe sua `SECRET_KEY`. Use uma chave forte e aleatória em produção.

---

## Rodando a Aplicação

Inicie o servidor FastAPI com:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

Para acessar a documentação interativa:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Autenticação

### POST /auth/user

Cria uma nova conta de usuário. **Requer autenticação de admin**.

Headers:

```
Authorization: Bearer <access_token>
```

Request (exemplo):

```json
{
  "nome": "João",
  "email": "joao@example.com",
  "senha": "senha_segura123",
  "ativo": true,
  "admin": false
}
```

Response 201 (exemplo):

```json
{
  "mensagem": "User created successfully joao@example.com"
}
```

Errors:

- 400: Usuário já existe
- 401: Token inválido ou expirado
- 403: Acesso negado (apenas admin)
- 422: Dados inválidos
- 500: Erro interno

---

### POST /auth/login

Autentica um usuário e retorna tokens de acesso e refresh.

Request (exemplo):

```json
{
  "email": "joao@example.com",
  "senha": "senha_segura123"
}
```

Response 200 (exemplo):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Errors:

- 404: Usuário não encontrado ou senha incorreta
- 401: Erro ao gerar token
- 500: Erro interno

---

### POST /auth/login-form

Autentica um usuário usando OAuth2 PasswordRequestForm. Retorna apenas o token de acesso.

**Content-Type**: `application/x-www-form-urlencoded`

Form Data:

```
username=joao@example.com
password=senha_segura123
```

Response 200 (exemplo):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer"
}
```

Errors:

- 404: Usuário não encontrado ou senha incorreta
- 401: Erro ao gerar token
- 500: Erro interno

---

### GET /auth/users

Lista todos os usuários do sistema. **Requer autenticação de admin**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "total": 2,
  "users": [
    {
      "id": 1,
      "nome": "maria",
      "email": "maria@gmail.com"
    },
    {
      "id": 2,
      "nome": "joao",
      "email": "joao@gmail.com"
    }
  ]
}
```

Errors:

- 401: Token inválido ou expirado
- 403: Acesso negado (apenas admin)
- 500: Erro interno

---

### GET /auth/refresh

Renova os tokens de acesso e refresh usando um token válido.

Headers:

```
Authorization: Bearer <refresh_token>
```

Response 200 (exemplo):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Errors:

- 401: Refresh token inválido ou expirado
- 500: Erro interno

---

## Pedidos

### **Orders**

#### GET /orders?status={status}

Lista pedidos. Parâmetro `status` opcional: `PENDENTE | CANCELADO | FINALIZADO`.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
[
  {
    "id": 1,
    "status": "CANCELADO",
    "id_usuario": 1,
    "preco": 25.5
  },
  {
    "id": 2,
    "status": "PENDENTE",
    "id_usuario": 1,
    "preco": 45.0
  }
]
```

Errors:

- 401: Não autenticado
- 422: Status inválido
- 500: Erro interno

---

#### POST /orders

Cria novo pedido para o usuário autenticado.

Headers:

```
Authorization: Bearer <access_token>
```

Request (exemplo):

```json
{
  "id_usuario": 1
}
```

Response 201 (exemplo):

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

Errors:

- 401: Não autenticado
- 422: Dados inválidos
- 500: Erro interno

---

#### POST /orders/cancel/{order_id}

Cancela um pedido (apenas admin ou dono do pedido).

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "message": "Order 1 canceled successfully",
  "order": {
    "id": 1,
    "status": "CANCELADO",
    "price": 25.5
  }
}
```

Errors:

- 401: Não autorizado
- 404: Pedido não encontrado
- 500: Erro interno

---

#### POST /orders/{order_id}/add_item

Adiciona item a um pedido.

Headers:

```
Authorization: Bearer <access_token>
```

Request (exemplo):

```json
{
  "quantidade": 2,
  "sabor": "Calabresa",
  "tamanho": "Médio",
  "preco_unitario": 25.0
}
```

Response 200 (exemplo):

```json
{
  "message": "Item added to order 1 successfully",
  "item": {
    "quantidade": 2,
    "sabor": "Calabresa",
    "tamanho": "Médio",
    "preco_pedido": 50.0
  }
}
```

Errors:

- 401: Não autenticado
- 404: Pedido não encontrado
- 422: Dados inválidos
- 500: Erro interno

---

#### DELETE /orders/delete_item/{order_item_id}

Remove um item de um pedido (apenas admin ou dono do pedido).

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "item_id": 1,
  "message": "Item successfully deleted.",
  "order_price": 50.0
}
```

Errors:

- 401: Não autorizado
- 404: Item ou pedido não encontrado
- 500: Erro interno

---

#### GET /orders/order?status={status}

Lista todos os pedidos do sistema. Parâmetro `status` opcional: `PENDENTE | CANCELADO | FINALIZADO`. **Requer autenticação de admin**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
[
  {
    "id": 1,
    "status": "PENDENTE",
    "id_usuario": 1,
    "preco": 45.0
  }
]
```

Errors:

- 401: Não autenticado
- 403: Acesso negado (apenas admin)
- 422: Status inválido
- 500: Erro interno

---

#### POST /orders/order

Cria um novo pedido para um usuário. **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Request (exemplo):

```json
{
  "id_usuario": 1
}
```

Response 201 (exemplo):

```json
{
  "message": "Create order: 5"
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 422: Dados inválidos
- 500: Erro interno

---

#### POST /orders/order/cancel/{order_id}

Cancela um pedido específico. **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "message": "Order 1 canceled successfully",
  "order": {
    "id": 1,
    "status": "CANCELADO",
    "price": 25.5
  }
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 404: Pedido não encontrado
- 500: Erro interno

---

#### POST /orders/order/add_item/{order_id}

Adiciona um item a um pedido específico. **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Request (exemplo):

```json
{
  "quantidade": 2,
  "sabor": "Calabresa",
  "tamanho": "Médio",
  "preco_unitario": 25.0
}
```

Response 200 (exemplo):

```json
{
  "message": "Item added to order 1 successfully",
  "item": {
    "quantidade": 2,
    "sabor": "Calabresa",
    "tamanho": "Médio",
    "preco_pedido": 50.0
  }
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 404: Pedido não encontrado
- 422: Dados inválidos
- 500: Erro interno

---

#### DELETE /orders/order/delete_item/{order_item_id}

Remove um item de um pedido. **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "item_id": 1,
  "message": "Item successfully deleted.",
  "order_price": 50.0
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 404: Item ou pedido não encontrado
- 500: Erro interno

---

#### POST /orders/order/finish/{order_id}

Finaliza um pedido (altera status para FINALIZADO). **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "message": "Order 1 finalized successfully",
  "order": {
    "id": 1,
    "status": "FINALIZADO",
    "preco": 50.0
  }
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 404: Pedido não encontrado
- 500: Erro interno

---

#### GET /orders/order/{order_id}

Obtém os detalhes completos de um pedido específico, incluindo a lista de itens. **Requer autenticação de admin ou dono do pedido**.

Headers:

```
Authorization: Bearer <access_token>
```

Response 200 (exemplo):

```json
{
  "quantity": 2,
  "order": {
    "id": 1,
    "status": "PENDENTE",
    "preco": 50.0,
    "itens": [
      {
        "quantidade": 2,
        "sabor": "Calabresa",
        "tamanho": "Médio",
        "preco_pedido": 50.0
      }
    ]
  }
}
```

Errors:

- 401: Não autenticado
- 403: Acesso negado
- 404: Pedido não encontrado
- 500: Erro interno

---

## Configuração de Autenticação

- **Tipo**: OAuth2 Password Bearer
- **Token URL**: `/auth/login-form`
- **Formato Header**: `Authorization: Bearer <token>`
- **Expiração de Token**: `ACCESS_TOKEN_EXPIRE_MINUTES` (padrão 30 min)
- **Refresh Token**: Válido por 7 dias

---

## Troubleshooting

| Erro                           | Causa                      | Solução                                                                |
| ------------------------------ | -------------------------- | ---------------------------------------------------------------------- |
| `SECRET_KEY não está definida` | .env ausente ou incompleto | Crie `app/.env` com SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES |
| `Logs vazios`                  | pasta `logs/` não existe   | Execute `mkdir logs` ou deixe a config criar automaticamente           |
| `401 Unauthorized`             | Token expirado ou inválido | Faça novo login em `/auth/login`                                       |
| `404 Not Found`                | Recurso não existe         | Confirme IDs de usuário/pedido existem                                 |
| `422 Validation Error`         | Dados inválidos            | Valide tipos e campos obrigatórios                                     |

---

## Referências

- FastAPI: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Passlib: https://passlib.readthedocs.io
- JWT (PyJWT): https://pyjwt.readthedocs.io
