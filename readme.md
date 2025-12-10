# Informações sobre a API

- `POST /api/users/register/` - Registrar novo usuário
- `POST /api/users/login/` - Fazer login
- `POST /api/users/token_rapido/` - Gerar token rápido
- `GET /api/users/` - Listar usuários

- `GET /api/products/` - Listar produtos
- `POST /api/products/` - Criar produto
- `PUT /api/products/{id}/` - Atualizar produto
- `DELETE /api/products/{id}/` - Deletar produto


- `GET /api/edited-items/` - Listar edições
- `POST /api/edited-items/` - Registrar edição


- `GET /api/quick-tokens/` - Listar tokens
- `POST /api/quick-tokens/` - Criar token


# Exemplos de uso da API

```bash
# Criar produto
curl -X POST http://localhost:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Produto",
    "quantidade": 100,
    "preco": 29.99,
    "volume": "1kg",
    "imagem": "https://..."
  }'

# Listar produtos
curl http://localhost:8000/api/products/

# Atualizar produto
curl -X PUT http://localhost:8000/api/products/1/ \
  -H "Content-Type: application/json" \
  -d '{"quantidade": 50}'



```
