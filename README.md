# 🛵 API de Delivery

API RESTful para gerenciamento de **pedidos**, **usuários** e **autenticação**.
Suporta fluxo completo de login, filtros de pedidos, cancelamento, migrações de banco via Alembic e autenticação baseada em **JWT**.

---

## 📁 Estrutura Geral das Rotas

* `/order` – Gerenciamento de pedidos
* `/auth` – Autenticação e gerenciamento de usuários
* `/refresh` – Renovação de token JWT

---

# 📦 **Módulo de Pedidos (`/order`)**

## **Listar pedidos**

Retorna todas as ordens cadastradas com suporte a filtros.

```http
GET /order
```

### **Query Params (opcionais):**

| Parâmetro | Tipo   | Descrição                                                 |
| --------- | ------ | --------------------------------------------------------- |
| `status`  | `list` | Filtra pedidos por: `PENDENTE`, `CANCELADO`, `FINALIZADO` |

---

## **Criar nova ordem**

Cria um pedido associado a um usuário existente.

```http
POST /order
```

### **Body (JSON):**

| Campo     | Tipo | Obrigatório | Descrição                 |
| --------- | ---- | ----------- | ------------------------- |
| `user_id` | int  | Sim         | ID do usuário solicitante |

> **Status:** Endpoint em evolução. Novos atributos (itens do pedido, endereço, pagamento etc.) serão adicionados futuramente.

---

## **Cancelar uma ordem**

```http
POST /order/cancel/{order_id}
```

### **Path Param:**

| Parâmetro  | Tipo | Obrigatório | Descrição                   |
| ---------- | ---- | ----------- | --------------------------- |
| `order_id` | int  | Sim         | ID da ordem a ser cancelada |

---

# 🔐 **Módulo de Autenticação (`/auth`)**

## **Login via JSON**

Autentica um usuário e retorna tokens JWT.

```http
POST /auth/login
```

### **Body (JSON):**

| Campo         | Tipo | Obrigatório |
| ------------- | ---- | ----------- |
| `user_schema` | dict | Sim         |

---

## **Listar usuários**

```http
GET /auth/users
```

Retorna todos os usuários cadastrados.

---

## **Login via formulário (OAuth2)**

```http
POST /auth/login-form
```

### **Body:**

| Campo    | Tipo | Obrigatório | Descrição                                         |
| -------- | ---- | ----------- | ------------------------------------------------- |
| `OAuth2` | dict | Sim         | Credenciais enviadas via formulário padrão OAuth2 |

---

# 🔄 **Atualizar token JWT**

Renova o token de acesso usando o refresh token.

```http
POST /refresh
```

### **Body:**

| Campo           | Tipo   | Obrigatório | Descrição          |
| --------------- | ------ | ----------- | ------------------ |
| `token_refresh` | bearer | Sim         | Token de renovação |

---

# 🚀 **Processo de Deploy**

Execute as migrações antes do deploy:

```bash
alembic revision --autogenerate -m "Descrição da migration"
alembic upgrade head
```

---

# 📚 **Referências**

* [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
* [Awesome README](https://github.com/matiassingers/awesome-readme)
* [How to Write a Good README](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)