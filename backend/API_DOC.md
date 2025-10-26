# Documentação

## Entrypoints HTTP

### Auth

#### POST /auth/login

* **Descrição:** Autentica o usuário e retorna um token JWT.
* **Body JSON:**

```json
{
  "username": "string",
  "password": "string"
}
```

* **Resposta 200:**

```json
{
  "access_token": "<JWT_TOKEN>"
}
```

* **Erros comuns:**

  * 400: JSON inválido ou ausente
  * 401: Credenciais inválidas

#### GET /auth/me

* **Descrição:** Retorna as informações do usuário autenticado.
* **Headers:**

  * Authorization: Bearer <JWT_TOKEN>
* **Resposta 200:**

```json
{
  "id": 1,
  "username": "admin",
  "roles": ["admin"]
}
```

* **Erros comuns:**

  * 401: Token inválido ou ausente
  * 404: Usuário não encontrado

### Admin

#### GET /admin/products

* **Descrição:** Lista todos os produtos cadastrados.
* **Requer:** role 'admin'
* **Resposta 200:**

```json
[
  {"id":1,"name":"Pizza","price":25.0},
  {"id":2,"name":"Burger","price":15.0}
]
```

#### POST /admin/products

* **Descrição:** Cria um novo produto.
* **Body JSON:**

```json
{
  "name": "string",
  "price": 0.0
}
```

* **Resposta 201:**

```json
{
  "id": 3,
  "name": "Salad",
  "price": 12.0
}
```

#### PUT /admin/products/<product_id>

* **Descrição:** Atualiza dados de um produto existente.
* **Body JSON:**

```json
{
  "name": "string",
  "price": 0.0
}
```

* **Resposta 200:**

```json
{
  "id": 1,
  "name": "Updated Pizza",
  "price": 27.0
}
```

#### POST /admin/users

* **Descrição:** Cria um novo usuário.
* **Body JSON:**

```json
{
  "username": "string",
  "password": "string",
  "roles": ["admin","waiter"]
}
```

* **Resposta 201:**

```json
{
  "id": 10,
  "username": "waiter1",
  "roles": ["waiter"]
}
```

#### PUT /admin/users/<user_id>

* **Descrição:** Atualiza dados de um usuário.
* **Body JSON:**

```json
{
  "username": "string",
  "roles": ["admin","kitchen"]
}
```

* **Resposta 200:**

```json
{
  "id": 10,
  "username": "updated_user",
  "roles": ["admin"]
}
```

### Waiter (Garçom)

#### GET /tables

* **Descrição:** Lista todas as mesas e status.
* **Requer:** role 'waiter' ou 'admin'
* **Resposta 200:**

```json
[
  {"id":1,"status":"OCCUPIED","number_of_people":4},
  {"id":2,"status":"FREE","number_of_people":0}
]
```

#### POST /tables/<table_id>/open

* **Descrição:** Abre uma mesa.
* **Body JSON:**

```json
{
  "number_of_people": 4
}
```

* **Resposta 200:**

```json
{
  "id":1,
  "status":"OCCUPIED",
  "number_of_people":4
}
```

#### GET /tables/<table_id>

* **Descrição:** Detalhes de uma mesa, incluindo pedidos.
* **Resposta 200:**

```json
{
  "id":1,
  "status":"OCCUPIED",
  "number_of_people":4,
  "orders":[
    {"id":101,"items":[{"product":"Pizza","quantity":2}]}]
}
```

#### POST /tables/<table_id>/close

* **Descrição:** Fecha uma mesa.
* **Resposta 200:**

```json
{
  "id":1,
  "status":"FREE",
  "number_of_people":0
}
```

#### POST /tables/<table_id>/orders

* **Descrição:** Cria pedido para mesa ocupada.
* **Body JSON:**

```json
{
  "items":[{"product_id":1,"quantity":2}]
}
```

* **Resposta 201:**

```json
{
  "id":101,
  "table_id":1,
  "items":[{"product":"Pizza","quantity":2}],
  "status":"PENDING"
}
```

#### POST /orders/<order_id>/items

* **Descrição:** Adiciona item a pedido existente.
* **Body JSON:**

```json
{
  "product_id":1,
  "quantity":1
}
```

* **Resposta 200:**

```json
{
  "id":101,
  "items":[{"product":"Pizza","quantity":3}],
  "status":"PENDING"
}
```

### Kitchen (Cozinha)

#### GET /kitchen/orders/pending

* **Descrição:** Lista todos os pedidos pendentes.
* **Resposta 200:**

```json
[
  {"id":101,"table_id":1,"status":"PENDING","items":[{"product":"Pizza","quantity":2}]}]
```

#### POST /kitchen/orders/<order_id>/start

* **Descrição:** Muda status do pedido para 'IN_PROGRESS'.
* **Resposta 200:**

```json
{
  "id":101,
  "status":"IN_PROGRESS"
}
```

#### POST /kitchen/orders/<order_id>/complete

* **Descrição:** Muda status do pedido para 'READY_FOR_DELIVERY'.
* **Resposta 200:**

```json
{
  "id":101,
  "status":"READY_FOR_DELIVERY"
}
```
