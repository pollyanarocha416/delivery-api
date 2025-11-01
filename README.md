
# API delivery-api

## Documentação da API

#### Retorna todos os itens

```http
  POST /order
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `api_key` | `string` | **Obrigatório**. A chave da sua API |

#### Criar ordem de serviço

```http
  POST /auth
```

| Parâmetro   | Tipo       | Descrição                                   |
| :---------- | :--------- | :------------------------------------------ |
| `usuario_schema` | `dict`|**Obrigatório** |

#### auth(usuario_schema)

Rota para criação de uma nova conta de usuário


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
