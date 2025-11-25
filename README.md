# API de delivery

#### Cria uma nova ordem de pedido

### Rota orders/
```http
  GET /order
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `status` | `list` | **Opcional**. Filtro por status literal 'PENDENTE', 'CANCELADO' ou 'FINALIZADO' |

```http
  POST /order
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `user_id` | `int` | **Obrigatório**. ID do usuario |

endpoint ainda em desenvolvimento...

## Cancela uma ordem
```http
  POST order/cancel/{order_id}
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `order_id` | `int` | **Obrigatório**. ID da ordem |


## Realiza o login de um usuario

### Rota /auth
```http
  POST /login
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `user_schema` | `dict`|**Obrigatório** |

## Realiza o login de um usuario via formulario

```http
  POST /login-form
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `OAuth2` | `dict`|**Obrigatório** |






## Rota para atualização do token jwt

```http
  POST /refresh
```
| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `token_refresh` | `bearer`|**Obrigatório** |



## Deploy

Para fazer o deploy desse projeto rode

```bash
    alembic revision --autogenerate -m "texto aqui..."

    alembic upgrade head
```
## Referência
 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
