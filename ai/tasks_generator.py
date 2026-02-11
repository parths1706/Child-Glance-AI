from ai.llm_client import ask_llm, clean_json_response
import json

def generate_daily_tasks(child_data, traits, tips):
    traits_text = "\n".join(t.get("title", "") for t in traits)
    tips_text = "\n".join(t.get("title", "") for t in tips)
    
    age_yrs = child_data.get("age_years", 0)
    age_mos = child_data.get("age_months", 0)
    age_desc = f"{age_yrs} years and {age_mos} months" if age_yrs or age_mos else "unknown age"
    country = child_data.get("country", "Unknown")

    prompt = f"""
You are the most fun Activity Boss ever! 🎮👾

TASK:
Give 4-6 super easy "Daily Missions" for a parent and child to do together.

RULES:
1. ZERO PREP: Every mission must be something they can do RIGHT NOW with no buying stuff or cleaning up. 🏡
2. BABY WORDS: Use tiny, easy words! No big adult words. 👶
3. SUPER FUN: Use TONS of emojis! Make it look like a party! 🎈🌈🍭✨
4. AGE FIT: Make sure a {age_desc} child can do it.
5. BONDING: Help them hug, laugh, and play! 🤗


FORMAT EXAMPLE:
[
  {{
    "title": "Tickle Monster Attack! 👾", 
    "description": "Counting to 3 and then giving gentle tickles! It makes everyone laugh! 😂✨"
  }}
]

CONTEXT:
Traits: {traits_text}
Parenting Focus (Tips): {tips_text}
Child Age: {age_desc}
Country: {country}
"""
    
    for _ in range(3):
        res = ask_llm(prompt)
        cleaned = clean_json_response(res)
        if cleaned:
            try:
                # Basic validation
                json.loads(cleaned)
                return res
            except:
                continue
    return ""
