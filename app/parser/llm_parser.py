import json
from openai import AsyncOpenAI
from app.config import settings

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are a price extraction assistant.
Given raw HTML or text from a product page, extract:
- product name
- price (numeric, no currency symbols)
- in_stock (true/false)

Respond ONLY with valid JSON: {"name": "...", "price": 0.0, "in_stock": true}
If you cannot find a value, use null."""


async def extract_with_llm(html: str) -> dict | None:
    # Trim HTML to avoid excessive token usage — send the first 8000 chars
    snippet = html[:8000]

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": snippet},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )

    try:
        result = json.loads(response.choices[0].message.content)
        result["source"] = "llm"
        return result
    except (json.JSONDecodeError, IndexError):
        return None
