import json
from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL, VALID_TIERS

_client = Groq(api_key=GROQ_API_KEY)

_SYSTEM_MESSAGE = """\
You are a safety classifier for home repair questions.

Classify each question into exactly one tier:

safe: Routine maintenance and low-risk cosmetic repairs that most homeowners can complete with basic tools and patience, with no realistic risk of injury, fire, flooding, or structural damage.

caution: Repairs a motivated homeowner might attempt on an existing fixture or system at the same location, where mistakes can cause meaningful cost or minor injury, but the task does not involve new wiring, new plumbing lines, gas work, structural changes, or work that normally requires a permit or licensed professional.

refuse: Repairs that could cause fire, flooding, structural failure, serious injury, or death if done incorrectly, or that involve gas lines, electrical panels, new circuits, main water lines, load-bearing structures, or other work that should be handled by a licensed professional or permitted contractor.

Apply this boundary carefully: if the task modifies hidden infrastructure or introduces a new electrical, plumbing, gas, or structural system, choose refuse; if it is a like-for-like replacement or minor repair on an existing fixture or component, choose caution.

Return exactly one JSON object with these keys:
tier: one of safe, caution, or refuse
reason: one short sentence explaining why that tier was chosen

Do not include markdown, code fences, extra keys, or extra text.\
"""


def classify_safety_tier(question: str) -> dict:
    """
    Classify a home repair question into one of three safety tiers.

    Returns a dict with:
      - "tier"   : str — one of "safe", "caution", "refuse"
      - "reason" : str — a brief explanation of why this tier was assigned
    """
    response = _client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_MESSAGE},
            {"role": "user", "content": f"Classify this home repair question: {question}"},
        ],
    )

    raw = response.choices[0].message.content.strip()

    try:
        data = json.loads(raw)
        tier = data.get("tier", "").lower().strip()
        reason = data.get("reason", "").strip()
        if tier not in VALID_TIERS or not reason:
            raise ValueError(f"invalid tier: {tier!r}")
        return {"tier": tier, "reason": reason}
    except Exception:
        return {
            "tier": "caution",
            "reason": "Could not reliably parse or validate the model output.",
        }
