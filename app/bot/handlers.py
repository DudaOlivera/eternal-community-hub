from datetime import datetime
import discord
import httpx

from app.config import settings

API_BASE = "http://api:8000"
# URL pública da API — usada para montar links de imagem acessíveis pelo Discord e pelo site
API_PUBLIC_URL = settings.SITE_BASE_URL.replace("https://eternal-server-sigma.vercel.app", "http://localhost:8000")


def is_staff(interaction: discord.Interaction) -> bool:
    return any(r.id == settings.DISCORD_STAFF_ROLE_ID for r in interaction.user.roles)


async def upload_attachment(attachment: discord.Attachment) -> str | None:
    """Download image from Discord CDN and upload to our API. Returns public URL."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Download from Discord immediately (URL expires fast)
            img_resp = await client.get(attachment.url)
            if img_resp.status_code != 200:
                return None

            # Upload to our API
            upload_resp = await client.post(
                f"{API_BASE}/api/upload",
                files={"file": (attachment.filename, img_resp.content, attachment.content_type)},
            )
            if upload_resp.status_code == 200:
                    data = upload_resp.json()
                    # Use public_url so Discord and site can access it
                    return data["public_url"]
    except Exception as e:
        print(f"[UPLOAD ERROR] {e}")
    return None


async def handle_news(interaction: discord.Interaction, titulo: str, conteudo: str, imagem: discord.Attachment = None):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    # Upload image immediately while Discord URL is still valid
    image_url = await upload_attachment(imagem) if imagem else None

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{API_BASE}/api/news", json={
            "title": titulo,
            "content": conteudo,
            "author": interaction.user.display_name,
            "use_ai": True,
            "image_url": image_url,
        })

    if resp.status_code == 201:
        await interaction.followup.send(
            f"✅ Notícia publicada!\n🔗 {settings.SITE_BASE_URL}/news.html",
            ephemeral=True,
        )
    else:
        await interaction.followup.send("❌ Erro ao publicar notícia.", ephemeral=True)


async def handle_event(interaction: discord.Interaction, nome: str, data: str, descricao: str, imagem: discord.Attachment = None):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    try:
        event_date = datetime.strptime(data, "%d/%m/%Y %H:%M").isoformat()
    except ValueError:
        await interaction.followup.send("❌ Formato de data inválido. Use DD/MM/YYYY HH:MM", ephemeral=True)
        return

    image_url = await upload_attachment(imagem) if imagem else None

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{API_BASE}/api/events", json={
            "name": nome,
            "description": descricao,
            "author": interaction.user.display_name,
            "event_date": event_date,
            "use_ai": True,
            "image_url": image_url,
        })

    if resp.status_code == 201:
        await interaction.followup.send(
            f"✅ Evento criado!\n🔗 {settings.SITE_BASE_URL}/news.html",
            ephemeral=True,
        )
    else:
        await interaction.followup.send("❌ Erro ao criar evento.", ephemeral=True)


async def handle_maintenance(interaction: discord.Interaction, motivo: str, duracao: str):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    async with httpx.AsyncClient(timeout=30.0) as client:
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
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{API_BASE}/api/ranking")

    if resp.status_code != 200:
        await interaction.followup.send("❌ Não foi possível obter o ranking.")
        return

    data = resp.json()
    if not data:
        await interaction.followup.send("📊 Nenhum dado de ranking disponível ainda. Volte mais tarde, guerreiro!")
        return

    lines = [f"**🏆 Ranking PvP** — [Ver no site]({settings.SITE_BASE_URL}/news.html)\n"]
    for i, p in enumerate(data[:10], 1):
        lines.append(f"`{i}.` **{p['player_name']}** ({p['char_class']}) — {p['pvp_kills']} kills")

    await interaction.followup.send("\n".join(lines))


async def handle_boss(interaction: discord.Interaction):
    await interaction.response.defer()
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{API_BASE}/api/server/bosses")

    data = resp.json()
    if not data:
        await interaction.followup.send("Nenhum boss agendado no momento.")
        return

    lines = [f"**💀 Próximos Boss Spawns** — [Ver no site]({settings.SITE_BASE_URL}/news.html)\n"]
    for b in data:
        lines.append(f"**{b['boss_name']}** — {b['location']} — `{b['spawn_time']}`")

    await interaction.followup.send("\n".join(lines))


async def handle_players(interaction: discord.Interaction):
    await interaction.response.defer()
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(f"{API_BASE}/api/server/status")

    data = resp.json()
    if data.get("online"):
        status = f"🟢 Online — [Ver no site]({settings.SITE_BASE_URL}/news.html)"
    else:
        reason = data.get("maintenance_reason", "")
        status = f"🔴 Em manutenção — {reason}"

    await interaction.followup.send(f"**Status do Servidor:** {status}")


async def handle_delete(interaction: discord.Interaction, resource: str):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    labels = {
        "news": "todas as notícias",
        "events": "todos os eventos",
        "all": "**TUDO** do banco de dados",
    }

    await interaction.response.defer(ephemeral=True)
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.delete(f"{API_BASE}/admin/{resource}")

    if resp.status_code == 200:
        await interaction.followup.send(
            f"🗑️ Apagado: {labels.get(resource, resource)}.", ephemeral=True
        )
    else:
        await interaction.followup.send("❌ Erro ao apagar.", ephemeral=True)


async def handle_limpar(interaction: discord.Interaction, quantidade: int):
    if not is_staff(interaction):
        await interaction.response.send_message("❌ Apenas a staff pode usar este comando.", ephemeral=True)
        return

    if quantidade < 1 or quantidade > 100:
        await interaction.response.send_message("❌ Quantidade deve ser entre 1 e 100.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    # Purge messages from the channel
    channel = interaction.channel
    deleted = await channel.purge(limit=quantidade)

    await interaction.followup.send(
        f"🗑️ {len(deleted)} mensagens apagadas do canal.", ephemeral=True
    )
