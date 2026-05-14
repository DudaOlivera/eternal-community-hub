from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_ENV: str = "development"
    SECRET_KEY: str = "changeme"
    DEBUG: bool = True

    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"

    # Site base URL (used to build post links sent to Discord)
    SITE_BASE_URL: str = "https://site.com"

    # Discord
    DISCORD_BOT_TOKEN: str
    DISCORD_GUILD_ID: int
    DISCORD_NEWS_CHANNEL_ID: int
    DISCORD_EVENTS_CHANNEL_ID: int
    DISCORD_MAINTENANCE_CHANNEL_ID: int
    DISCORD_SUPPORT_CHANNEL_ID: int
    DISCORD_RANKING_CHANNEL_ID: int
    DISCORD_STAFF_ROLE_ID: int

    # Gemini (Google AI)
    OPENAI_API_KEY: str  # mantido como nome genérico para não quebrar o .env
    OPENAI_MODEL: str = "gemini-1.5-flash"

    # Game Server
    GAME_SERVER_API_URL: str = ""
    GAME_SERVER_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
