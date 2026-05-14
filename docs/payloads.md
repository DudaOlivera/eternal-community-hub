# Exemplos de Payloads

## POST /api/news

```json
{
  "title": "Atualização 1.5 disponível",
  "content": "vai ter update hoje à noite com novos itens e balanceamento de classes",
  "author": "GM Kira",
  "use_ai": true
}
```

Resposta:
```json
{
  "id": 1,
  "title": "Atualização 1.5 disponível",
  "slug": "atualizacao-1-5-disponivel",
  "content": "vai ter update hoje à noite com novos itens e balanceamento de classes",
  "ai_content": "Guerreiros de Aden! A grande Atualização 1.5 chega esta noite, trazendo novos itens épicos e o reequilíbrio das classes. Preparem-se para uma nova era de batalhas!",
  "author": "GM Kira",
  "published": true,
  "sent_discord": true,
  "created_at": "2024-01-15T20:00:00"
}
```

O Discord recebe automaticamente:
```
📰 Atualização 1.5 disponível
Guerreiros de Aden! A grande Atualização 1.5 chega esta noite...
🔗 Leia mais: https://site.com/news/atualizacao-1-5-disponivel
```

---

## POST /api/events

```json
{
  "name": "Torneio PvP",
  "description": "vai ter evento pvp domingo 20h com premiação",
  "author": "GM Kira",
  "event_date": "2024-01-21T20:00:00",
  "use_ai": true
}
```

---

## POST /api/maintenance

```json
{
  "reason": "Atualização de segurança e correção de bugs críticos",
  "estimated_duration": "2 horas",
  "author": "GM Kira"
}
```

---

## POST /api/maintenance/finish

```json
{
  "maintenance_id": 1
}
```

---

## POST /api/support

```json
{
  "player_name": "Aragorn",
  "discord_user_id": "123456789",
  "message": "meu personagem sumiu depois do update, preciso de ajuda"
}
```

---

## POST /api/support/reply

```json
{
  "ticket_id": 1,
  "response": "Olá! Identificamos o problema e seu personagem foi restaurado. Por favor, reconecte ao servidor."
}
```

---

## GET /api/server/status

```json
{
  "online": true,
  "maintenance": false,
  "maintenance_reason": null
}
```
