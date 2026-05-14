import json
import google.generativeai as genai

from app.config import settings

genai.configure(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = (
    "Você é o comunicador oficial do servidor privado de Lineage 2. "
    "Seu estilo é épico, medieval e fantástico, como os anúncios do jogo. "
    "Transforme mensagens simples em comunicados profissionais e envolventes. "
    "Use termos do universo de Lineage 2 como: guerreiros, Aden, Elmore, batalha, honra, glória. "
    "Seja conciso mas impactante."
)


async def enhance_announcement(raw_text: str, content_type: str = "notícia") -> str:
    """Transform a simple staff message into a professional announcement."""
    model = genai.GenerativeModel(
        model_name=settings.OPENAI_MODEL,
        system_instruction=SYSTEM_PROMPT,
    )

    prompt = (
        f"Transforme este rascunho de {content_type} em um comunicado épico para a comunidade:\n\n"
        f'"{raw_text}"\n\n'
        "Retorne apenas o texto final, sem explicações."
    )

    response = await model.generate_content_async(prompt)
    return response.text.strip()


async def classify_support_message(message: str) -> dict:
    """Classify a support message and suggest a response."""
    model = genai.GenerativeModel(model_name=settings.OPENAI_MODEL)

    prompt = (
        f"Analise esta mensagem de suporte de um player:\n\n\"{message}\"\n\n"
        "Retorne um JSON com:\n"
        "- priority: low/medium/high/urgent\n"
        "- category: bug/account/pvp/event/other\n"
        "- suggested_response: resposta sugerida em português\n"
        "Retorne apenas o JSON puro, sem markdown, sem blocos de código."
    )

    response = await model.generate_content_async(prompt)
    try:
        return json.loads(response.text.strip())
    except json.JSONDecodeError:
        return {"priority": "medium", "category": "other", "suggested_response": ""}
