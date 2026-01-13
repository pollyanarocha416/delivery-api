# 🛵 API de Delivery

API para gerenciamento de pedidos, usuários e autenticação (JWT). Projeto em FastAPI + SQLAlchemy (SQLite) com logging configurável.

## Índice

- Pré-requisitos
- Setup
- Variáveis de ambiente
- Rodando a aplicação
- Logging
- Banco de dados / Migrações

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

### **Endpoints adicionais de Pedido (novos)**

Os endpoints abaixo foram adicionados ao router `/orders` usando o subcaminho `/order`. Todos exigem `Authorization: Bearer <access_token>`.

- GET `/orders/order` — lista todos os pedidos (apenas admin). Query opcional: `status=PENDENTE|CANCELADO|FINALIZADO`.

  Exemplo de resposta 200:

  ```json
  [{ "id": 1, "status": "PENDENTE", "id_usuario": 1, "preco": 45.0 }]
  ```

- POST `/orders/order` — cria um novo pedido para `id_usuario` (admin ou dono).

  Request exemplo:

  ```json
  { "id_usuario": 1 }
  ```

  Response 201 exemplo:

  ```json
  { "message": "Create order: 5" }
  ```

- POST `/orders/order/cancel/{order_id}` — cancela um pedido (admin ou dono).

  Exemplo de response 200:

  ```json
  {
    "message": "Order 1 canceled successfully",
    "order": { "id": 1, "status": "CANCELADO", "price": 25.5 }
  }
  ```

- POST `/orders/order/add_item/{order_id}` — adiciona item a um pedido (admin ou dono).

  Request exemplo:

  ```json
  {
    "quantidade": 2,
    "sabor": "Calabresa",
    "tamanho": "Médio",
    "preco_unitario": 25.0
  }
  ```

  Response 200 exemplo:

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

- DELETE `/orders/order/delete_item/{order_item_id}` — remove um item de um pedido (admin ou dono).

  Response 200 exemplo:

  ```json
  { "item_id": 1, "message": "Item successfully deleted.", "order_price": 50.0 }
  ```

- POST `/orders/order/finish/{order_id}` — finaliza um pedido (admin ou dono).

  Response 200 exemplo:

  ```json
  {
    "message": "Order 1 finalized successfully",
    "order": { "id": 1, "status": "FINALIZADO", "preco": 50.0 }
  }
  ```

- GET `/orders/order/{order_id}` — obtém detalhes do pedido (admin ou dono). A resposta inclui `quantity` e `order` com `itens`.

  Response 200 exemplo (trecho):

  ```json
  {"quantity":2, "order": {"id":1, "status":"PENDENTE", "preco":50.0, "itens":[...]}}
  ```

---

## Autenticação

- Tipo: OAuth2 Password Bearer
- Token URL: `/auth/login-form`
- Formato Header: `Authorization: Bearer <token>`
- Token válido por: `ACCESS_TOKEN_EXPIRE_MINUTES` (padrão 30 min)

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
