from ai.llm_client import ask_llm, clean_json_response
import json

def generate_parenting_tips(child_data, selected_traits):
    """
    selected_traits = FINAL traits chosen by the parent
    (after removals and additions)
    """
   
    traits_text = "\n".join(
        f"- {t.get('title', 'Trait')}: {t.get('description', '')}"
        for t in selected_traits
    )

    prompt = f"""
You are the world's best and most fun parenting coach! 🌟🦄

TASK:
Give 4-6 super simple parenting tips. 

RULES:
1. VERY SIMPLE WORDS: Use words so easy that even a child could understand! No "fancy" or "expert" talk. 👶
2. FUN & PLAYFUL: Write like a fun cartoon! Use LOTS of emojis! 🎈🌈🍭
3. ASTROLOGY MAGIC: Since this child is from {child_data.get("country", "")}, include tips about their horoscope or moon alignment if it's in their traits! ✨🌙
4. BRIEF BUT SIMPLE : Keep each tip 4-5 sentences in explain tips what to do and how to do .
5. NO FILLER: Just the JSON list.

FORMAT EXAMPLE:
[
  {{
    "title": "Happy Moon Time! 🌙",
    "description": "Your child is sensitive like the moon! Give them a big hug and speak softly tonight. It makes them feel safe! 🤗✨"
  }}
]

CONTEXT:
Traits & Insights: {traits_text}
Child Age: {child_data.get("age_years", 0)} years
Country: {child_data.get("country", "")}
"""

    for _ in range(3):
        res = ask_llm(prompt)
        cleaned = clean_json_response(res)
        if cleaned:
            try:
                json.loads(cleaned)
                return res
            except:
                continue
    return ""