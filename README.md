# NOC Template

Projeto baseado em FastAPI + React, com Docker Compose separado por stack de backend e frontend.

O objetivo atual é manter uma base limpa para evoluir a API com endpoints próprios, inclusive consultas a fontes externas, preservando uma UI React e documentação OpenAPI acessível pelo navegador.

## Stack

### Backend

- FastAPI
- SQLModel
- Pydantic / Pydantic Settings
- PostgreSQL 18
- Alembic
- Pytest
- Uvicorn/FastAPI CLI

### Frontend

- React
- TypeScript
- Vite
- TanStack Router
- TanStack Query
- Tailwind CSS
- shadcn/ui
- Nginx

### Infraestrutura Local

- Docker Compose
- Compose backend: [compose.backend.yml](./compose.backend.yml)
- Compose frontend: [compose.frontend.yml](./compose.frontend.yml)
- Makefile operacional: [backend/Makefile](./backend/Makefile)
- Reverse proxy via Nginx do frontend

## Arquitetura Docker

### `compose.backend.yml`

Serviços:

- `db`: PostgreSQL 18 na porta `5432`.
- `backend`: API FastAPI na porta `8000`.
- `adminer`: UI opcional para administrar o banco, habilitada pelo profile `tools`.

O backend executa automaticamente:

```bash
bash scripts/prestart.sh
```

Esse script aguarda o banco, roda migrations com Alembic e cria dados iniciais.

### `compose.frontend.yml`

Serviço:

- `frontend`: build React servido por Nginx na porta `5173`.

O Nginx do frontend também funciona como reverse proxy:

- `/api` -> `backend:8000`
- `/docs` -> Swagger UI do backend
- `/redoc` -> ReDoc do backend
- `/swagger` -> redireciona para `/docs`

## Como Rodar

Os comandos principais estão no [backend/Makefile](./backend/Makefile). Rode a partir da pasta `backend`:

```bash
cd backend
make up
```

Isso executa:

```bash
docker compose --env-file ../.env -f ../compose.backend.yml -f ../compose.frontend.yml up --build -d
```

Para parar e remover volumes:

```bash
make down
```

Para subir apenas o backend:

```bash
make up-backend
```

Para subir apenas o frontend:

```bash
make up-frontend
```

Para acompanhar logs:

```bash
make logs
```

Para acompanhar apenas o backend:

```bash
make logs-backend
```

Para abrir shell no container do backend:

```bash
make shell
```

## Rotas no Navegador

Com `make up`, acesse:

```text
Frontend
http://localhost:5173

Swagger UI via reverse proxy
http://localhost:5173/docs

Alias do Swagger
http://localhost:5173/swagger

ReDoc via reverse proxy
http://localhost:5173/redoc

API via reverse proxy
http://localhost:5173/api/v1

Health check via reverse proxy
http://localhost:5173/api/v1/utils/health-check/

Backend direto
http://localhost:8000

Swagger direto no backend
http://localhost:8000/docs

Health check direto no backend
http://localhost:8000/api/v1/utils/health-check/
```

Adminer não sobe por padrão. Para iniciar:

```bash
cd backend
docker compose --env-file ../.env -f ../compose.backend.yml --profile tools up -d adminer
```

Depois acesse:

```text
http://localhost:8080
```

## Testes

Com a stack backend rodando:

```bash
cd backend
make test
```

Para passar argumentos ao Pytest:

```bash
make test PYTEST_ARGS="-x"
```

Para recriar a stack backend antes dos testes:

```bash
make test-fresh
```

## Banco de Dados

Aplicar migrations:

```bash
cd backend
make db-migrate
```

Criar dados iniciais:

```bash
make db-seed
```

Abrir `psql` no container do banco:

```bash
make db-shell
```

Limpar schema, rodar migrations e recriar dados iniciais:

```bash
make db-clean
```

Recriar a stack backend removendo o volume do banco:

```bash
make db-reset
```

## Limpeza Docker

Esses comandos removem recursos Docker locais. Use com cuidado.

```bash
cd backend

make prune
make prune-volumes
make prune-images
make prune-all
```

Equivalências:

```bash
make prune          # docker system prune -a
make prune-volumes  # docker volume prune
make prune-images   # docker image prune -a
make prune-all      # docker system prune -a --volumes
```

## Variáveis de Ambiente

As variáveis ficam no arquivo [.env](./.env). Para ambiente local, os valores `changethis` funcionam, mas geram avisos no backend.

Antes de staging ou produção, troque pelo menos:

- `SECRET_KEY`
- `POSTGRES_PASSWORD`

Gere secrets com:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Documentação Complementar

- Backend: [backend/README.md](./backend/README.md)
- Frontend: [frontend/README.md](./frontend/README.md)
- Desenvolvimento: [development.md](./development.md)
- Deploy: [deployment.md](./deployment.md)
