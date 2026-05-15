import httpx
from app.config import settings

DISCORD_API = "https://discord.com/api/v10"


async def send_message(channel_id: int, content: str = "", embed: dict | None = None) -> bool:
    """Send a message to a Discord channel via REST API."""
    headers = {
        "Authorization": f"Bot {settings.DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json",
    }
    payload: dict = {"content": content}
    if embed:
        payload["embeds"] = [embed]

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            json=payload,
            headers=headers,
        )
        return resp.status_code == 200


# --- Embed builders ---

def build_news_embed(title: str, content: str, author: str, site_url: str, image_url: str = None) -> dict:
    embed = {
        "title": f"📰 {title}",
        "description": content[:300] + ("..." if len(content) > 300 else ""),
        "url": site_url,
        "color": 0xFFD700,
        "fields": [{"name": "🔗 Leia mais", "value": site_url, "inline": False}],
        "footer": {"text": f"Publicado por {author} • Lineage 2 Community Hub"},
    }
    if image_url:
        embed["image"] = {"url": image_url}
    return embed


def build_event_embed(name: str, description: str, event_date: str, author: str, site_url: str, image_url: str = None) -> dict:
    embed = {
        "title": f"⚔️ {name}",
        "description": description[:300] + ("..." if len(description) > 300 else ""),
        "url": site_url,
        "color": 0x8B0000,
        "fields": [
            {"name": "📅 Data", "value": event_date, "inline": True},
            {"name": "🔗 Saiba mais", "value": site_url, "inline": False},
        ],
        "footer": {"text": f"Criado por {author} • Lineage 2 Community Hub"},
    }
    if image_url:
        embed["image"] = {"url": image_url}
    return embed


def build_maintenance_embed(reason: str, duration: str, author: str) -> dict:
    return {
        "title": "🔧 Manutenção Programada",
        "description": reason,
        "color": 0xFF4500,
        "fields": [{"name": "⏱️ Duração estimada", "value": duration, "inline": True}],
        "footer": {"text": f"Anunciado por {author} • Lineage 2 Community Hub"},
    }


def build_maintenance_end_embed() -> dict:
    return {
        "title": "✅ Servidor Online",
        "description": "O servidor voltou ao ar! Bem-vindos de volta, guerreiros de Aden!",
        "color": 0x00FF00,
    }


def build_boss_embed(boss_name: str, location: str, spawn_time: str) -> dict:
    return {
        "title": f"💀 Boss Spawn: {boss_name}",
        "description": f"Prepare-se, guerreiros! **{boss_name}** está prestes a aparecer!",
        "color": 0x800080,
        "fields": [
            {"name": "📍 Local", "value": location, "inline": True},
            {"name": "⏰ Horário", "value": spawn_time, "inline": True},
        ],
        "footer": {"text": "Lineage 2 Community Hub"},
    }


def build_support_embed(ticket_id: int, player_name: str, message: str, priority: str, suggested: str) -> dict:
    return {
        "title": f"🎫 Novo Ticket #{ticket_id}",
        "description": message,
        "color": 0x00BFFF,
        "fields": [
            {"name": "👤 Player", "value": player_name, "inline": True},
            {"name": "⚠️ Prioridade", "value": priority.upper(), "inline": True},
            {"name": "🤖 Resposta sugerida", "value": suggested or "N/A", "inline": False},
        ],
        "footer": {"text": f"Responda com /responder {ticket_id} [mensagem]"},
    }
