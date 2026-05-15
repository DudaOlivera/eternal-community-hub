import logging
import discord
from discord.ext import commands
from discord import app_commands

from app.config import settings
from app.bot import handlers

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("bot")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

GUILD = discord.Object(id=settings.DISCORD_GUILD_ID)


@bot.event
async def on_ready():
    log.info(f"Logado como {bot.user} (ID: {bot.user.id})")
    try:
        tree.copy_global_to(guild=GUILD)
        synced = await tree.sync(guild=GUILD)
        log.info(f"{len(synced)} comandos sincronizados no servidor {settings.DISCORD_GUILD_ID}")
        for cmd in synced:
            log.info(f"  -> /{cmd.name}")
    except Exception as e:
        log.error(f"ERRO ao sincronizar comandos: {e}", exc_info=True)


@tree.command(name="news", description="Publicar uma notícia", guild=GUILD)
@app_commands.describe(titulo="Título da notícia", conteudo="Conteúdo da notícia", imagem="Anexe uma imagem (opcional)")
async def cmd_news(interaction: discord.Interaction, titulo: str, conteudo: str, imagem: discord.Attachment = None):
    await handlers.handle_news(interaction, titulo, conteudo, imagem)


@tree.command(name="evento", description="Criar um evento", guild=GUILD)
@app_commands.describe(nome="Nome do evento", data="Data (DD/MM/YYYY HH:MM)", descricao="Descrição", imagem="Anexe uma imagem (opcional)")
async def cmd_evento(interaction: discord.Interaction, nome: str, data: str, descricao: str, imagem: discord.Attachment = None):
    await handlers.handle_event(interaction, nome, data, descricao, imagem)


@tree.command(name="manutencao", description="Anunciar manutenção", guild=GUILD)
@app_commands.describe(motivo="Motivo da manutenção", duracao="Duração estimada")
async def cmd_manutencao(interaction: discord.Interaction, motivo: str, duracao: str):
    await handlers.handle_maintenance(interaction, motivo, duracao)


@tree.command(name="ranking", description="Ver ranking PvP", guild=GUILD)
async def cmd_ranking(interaction: discord.Interaction):
    await handlers.handle_ranking(interaction)


@tree.command(name="boss", description="Ver próximos boss spawns", guild=GUILD)
async def cmd_boss(interaction: discord.Interaction):
    await handlers.handle_boss(interaction)


@tree.command(name="players", description="Ver status do servidor", guild=GUILD)
async def cmd_players(interaction: discord.Interaction):
    await handlers.handle_players(interaction)


@tree.command(name="limpar", description="Apagar últimas mensagens do canal", guild=GUILD)
@app_commands.describe(quantidade="Quantas mensagens apagar (máx 100)")
async def cmd_limpar(interaction: discord.Interaction, quantidade: int = 10):
    await handlers.handle_limpar(interaction, quantidade)


@tree.command(name="apagar_news", description="Apagar todas as notícias do banco", guild=GUILD)
async def cmd_apagar_news(interaction: discord.Interaction):
    await handlers.handle_delete(interaction, "news")


@tree.command(name="apagar_eventos", description="Apagar todos os eventos do banco", guild=GUILD)
async def cmd_apagar_eventos(interaction: discord.Interaction):
    await handlers.handle_delete(interaction, "events")


@tree.command(name="apagar_tudo", description="⚠️ Apagar TUDO do banco de dados", guild=GUILD)
async def cmd_apagar_tudo(interaction: discord.Interaction):
    await handlers.handle_delete(interaction, "all")

if __name__ == "__main__":
    bot.run(settings.DISCORD_BOT_TOKEN)
