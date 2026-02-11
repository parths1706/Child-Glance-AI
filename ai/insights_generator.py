from ai.llm_client import ask_llm

def generate_insights(child_data):
    is_indian = child_data.get("country", "") == "India"

    context_instruction = ""
    if is_indian:
        context_instruction = """
        IMPORTANT INDIAN CONTEXT:
        - Use Indian birth timing traditions ONLY as soft cultural tendencies.
        - Do NOT mention astrology terms, planets, rashis, nakshatras.
        - Frame insights as:
          "Children born around this time often show..."
          "A commonly observed early-life tendency is..."
        - NO destiny, NO future prediction.
        - Focus on emotional needs, temperament, and learning style.
        """

    prompt = f"""
You are a child development expert combining behavioral psychology
and culturally-aware parenting insights.

TASK:
Generate 4–5 short "Child Glance" insights for a parent.

{context_instruction}

WHAT THESE INSIGHTS ARE:
- Observed personality tendencies
- Emotional patterns
- Learning or social preferences
- Helpful for understanding a child today

OUTPUT FORMAT (STRICT JSON LIST ONLY):
[
  {{
    "id": "unique_trait_id_snake_case",
    "category": "Personality | Emotional | Learning | Social",
    "title": "Short Trait Title",
    "description": "One short sentence (max 8 words).",
    "source": "cultural_tendency | behavioral_psychology"
  }}
]

RULES:
- Calm, warm, modern tone
- NO medical claims
- NO future predictions
- NO negative framing
- NO extra text outside JSON

CHILD PROFILE:
- Age: {child_data.get("age_years", 0)} years, {child_data.get("age_months", 0)} months
- DOB: {child_data.get("dob")}
- Birth Time: {child_data.get("birth_time", "Not provided")}
- Location: {child_data.get("city")}, {child_data.get("country")}
"""

    return ask_llm(prompt)

def suggest_additional_traits(child_data):
    is_indian = child_data.get("country", "") == "India"
    
    prompt = f"""
    You are a child development expert. Based on the profile below, suggest 6-8 short personality traits 
    or emotional tendencies that PARENTS often notice or want to know about.
    
    CHILD PROFILE:
    - Age: {child_data.get("age_years", 0)}y {child_data.get("age_months", 0)}m
    - Location: {child_data.get("country")}
    
    {"(Include traits common in Indian cultural context but frame them behaviorally)" if is_indian else ""}
    
    OUTPUT: A simple comma-separated list of short names (e.g., Selective Eater, Quick Learner, High Energy).
    NO extra text.
    """
    return ask_llm(prompt).split(",")

def generate_specific_insight(child_data, trait_name):
    is_indian = child_data.get("country", "") == "India"
    
    prompt = f"""
    Generate ONE child personality insight in JSON format for the trait: "{trait_name}".
    
    CHILD PROFILE:
    - Age: {child_data.get("age_years", 0)}y {child_data.get("age_months", 0)}m
    - Location: {child_data.get("country")}
    
    JSON FORMAT:
    {{
      "id": "unique_string",
      "category": "Personality | Emotional | Learning | Social",
      "title": "{trait_name}",
      "description": "One short sentence (max 8 words).",
      "source": "cultural_tendency | behavioral_psychology"
    }}
    
    RULES: Warm tone, positive framing, ONLY JSON output.
    """
    return ask_llm(prompt)
