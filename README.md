# delivery-api

#### Cria uma nova ordem

```http
  POST /order
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Obrigatório**. A chave da sua API |

#### Criar um novo usuario

```http
  POST /auth
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `user_schema` | `dict`|**Obrigatório** |

#### auth(usuario_schema)

#### Atualiza token de login

```http
  POST auth/refresh
```
| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `token_refresh` | `bearer`|**Obrigatório** |

Rota para atualização do token de login


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
