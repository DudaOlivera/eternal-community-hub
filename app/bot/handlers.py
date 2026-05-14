from datetime import datetime
import discord
import httpx

from app.config import settings

API_BASE = "http://api:8000"


def is_staff(interaction: discord.Interaction) -> bool:
    return any(r.id == settings.DISCORD_STAFF_ROLE_ID for r in interaction.user.roles)


async def handle_news(interaction: discord.Interaction, titulo: str, conteudo: str):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/api/news", json={
            "title": titulo,
            "content": conteudo,
            "author": interaction.user.display_name,
            "use_ai": True,
        })

    if resp.status_code == 201:
        data = resp.json()
        await interaction.followup.send(
            f"✅ Notícia publicada!\n🔗 {settings.SITE_BASE_URL}/news/{data['slug']}",
            ephemeral=True,
        )
    else:
        await interaction.followup.send("❌ Erro ao publicar notícia.", ephemeral=True)


async def handle_event(interaction: discord.Interaction, nome: str, data: str, descricao: str):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    try:
        event_date = datetime.strptime(data, "%d/%m/%Y %H:%M").isoformat()
    except ValueError:
        await interaction.followup.send("❌ Formato de data inválido. Use DD/MM/YYYY HH:MM", ephemeral=True)
        return

    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/api/events", json={
            "name": nome,
            "description": descricao,
            "author": interaction.user.display_name,
            "event_date": event_date,
            "use_ai": True,
        })

    if resp.status_code == 201:
        event_data = resp.json()
        await interaction.followup.send(
            f"✅ Evento criado!\n🔗 {settings.SITE_BASE_URL}/events/{event_data['slug']}",
            ephemeral=True,
        )
    else:
        await interaction.followup.send("❌ Erro ao criar evento.", ephemeral=True)


async def handle_maintenance(interaction: discord.Interaction, motivo: str, duracao: str):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/api/maintenance", json={
            "reason": motivo,
            "estimated_duration": duracao,
            "author": interaction.user.display_name,
        })

    if resp.status_code == 201:
        await interaction.followup.send("✅ Manutenção anunciada em todos os canais!", ephemeral=True)
    else:
        await interaction.followup.send("❌ Erro ao anunciar manutenção.", ephemeral=True)


async def handle_ranking(interaction: discord.Interaction):
    await interaction.response.defer()
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/api/ranking")

    if resp.status_code != 200:
        await interaction.followup.send("❌ Não foi possível obter o ranking.")
        return

    data = resp.json()
    if not data:
        await interaction.followup.send("Nenhum dado de ranking disponível.")
        return

    lines = [f"**🏆 Ranking PvP** — [Ver no site]({settings.SITE_BASE_URL}/ranking)\n"]
    for i, p in enumerate(data[:10], 1):
        lines.append(f"`{i}.` **{p['player_name']}** ({p['char_class']}) — {p['pvp_kills']} kills")

    await interaction.followup.send("\n".join(lines))


async def handle_boss(interaction: discord.Interaction):
    await interaction.response.defer()
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/api/server/bosses")

    data = resp.json()
    if not data:
        await interaction.followup.send("Nenhum boss agendado no momento.")
        return

    lines = [f"**💀 Próximos Boss Spawns** — [Ver no site]({settings.SITE_BASE_URL}/bosses)\n"]
    for b in data:
        lines.append(f"**{b['boss_name']}** — {b['location']} — `{b['spawn_time']}`")

    await interaction.followup.send("\n".join(lines))


async def handle_players(interaction: discord.Interaction):
    await interaction.response.defer()
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/api/server/status")

    data = resp.json()
    if data.get("online"):
        status = f"🟢 Online — [Ver no site]({settings.SITE_BASE_URL}/status)"
    else:
        reason = data.get("maintenance_reason", "")
        status = f"🔴 Em manutenção — {reason}"

    await interaction.followup.send(f"**Status do Servidor:** {status}")
