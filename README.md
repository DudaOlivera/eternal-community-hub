# Lineage 2 Community Hub

Sistema integrado para comunidade de servidor privado de Lineage 2, conectando Discord e site oficial com automação e IA.

## Fluxo principal

```
Staff publica via Discord (/news) ou Painel Admin
              ↓
        FastAPI (back-end)
              ↓
     Salva no PostgreSQL
              ↓
   ┌──────────┴──────────┐
   ↓                     ↓
Discord              Site oficial
(embed com link)   (consome a API)
```

## Stack

- **Backend:** Python 3.11 + FastAPI
- **Bot Discord:** discord.py
- **Banco:** PostgreSQL + SQLAlchemy (async)
- **Cache/Filas:** Redis + Celery
- **IA:** OpenAI API (GPT-4o-mini)
- **Infra:** Docker + Docker Compose

## Estrutura de Pastas

```
lineage2-community-hub/
├── app/
│   ├── api/              # Rotas FastAPI
│   ├── bot/              # Discord bot (slash commands + handlers)
│   ├── services/         # Lógica de negócio
│   ├── integrations/     # Discord REST, OpenAI
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── tasks/            # Celery (boss spawns, lembretes)
│   └── utils/            # Helpers (slug, etc.)
├── migrations/           # Alembic
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## Como Rodar

```bash
git clone https://github.com/seu-usuario/lineage2-community-hub
cd lineage2-community-hub
cp .env.example .env
# Preencha o .env com suas credenciais

docker-compose up -d
docker-compose exec api alembic revision --autogenerate -m "initial"
docker-compose exec api alembic upgrade head
```

- API + Docs: http://localhost:8000/docs

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /api/news | Criar notícia (salva + publica no Discord) |
| GET | /api/news | Listar notícias (consumido pelo site) |
| GET | /api/news/{slug} | Detalhe da notícia |
| POST | /api/events | Criar evento |
| GET | /api/events | Listar eventos |
| GET | /api/events/{slug} | Detalhe do evento |
| POST | /api/maintenance | Iniciar manutenção |
| POST | /api/maintenance/finish | Encerrar manutenção |
| GET | /api/maintenance/active | Manutenção ativa |
| GET | /api/server/status | Status do servidor |
| GET | /api/server/bosses | Próximos boss spawns |
| GET | /api/ranking | Ranking PvP |
| POST | /api/support | Abrir ticket de suporte |
| POST | /api/support/reply | Staff responde ticket |

## Comandos Discord

| Comando | Quem pode usar | Descrição |
|---------|---------------|-----------|
| `/news [título] [conteúdo]` | Staff | Publica notícia + envia embed com link |
| `/evento [nome] [data] [descrição]` | Staff | Cria evento + envia embed com link |
| `/manutencao [motivo] [duração]` | Staff | Anuncia manutenção |
| `/ranking` | Todos | Exibe top 10 PvP |
| `/boss` | Todos | Lista próximos boss spawns |
| `/players` | Todos | Status do servidor |

## Integração com o Site

O site consome a API via GET. Exemplos:

```js
// Listar notícias
fetch('http://localhost:8000/api/news')

// Detalhe de uma notícia
fetch('http://localhost:8000/api/news/abertura-oficial')

// Status do servidor
fetch('http://localhost:8000/api/server/status')
```

Configure `SITE_BASE_URL` no `.env` para que os links enviados no Discord apontem para o seu site.

## Variáveis de Ambiente

Veja `.env.example`.

## Licença

MIT
