from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

# Webhooks reservados para integrações futuras (ex: game server callbacks)
