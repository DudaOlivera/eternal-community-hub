from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import news, events, maintenance, support, server, webhooks, ranking, upload, admin

app = FastAPI(
    title="Lineage 2 Community Hub",
    description="Sistema integrado para comunidade de servidor privado de Lineage 2",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://eternal-server-sigma.vercel.app",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(events.router)
app.include_router(maintenance.router)
app.include_router(support.router)
app.include_router(server.router)
app.include_router(ranking.router)
app.include_router(upload.router)
app.include_router(admin.router)
app.include_router(webhooks.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "Lineage 2 Community Hub"}
