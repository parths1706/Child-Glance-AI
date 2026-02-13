from ai.llm_client import ask_llm, clean_json_response
import json
import streamlit as st

def generate_comprehensive_report(child_data):
    """
    Generates a complete astrology-based report including:
    - Sun & Moon Signs
    - Core Personality, Emotional Needs, Strengths, Growth Areas
    - Daily Parenting Tip
    - Structured Daily Micro-Tasks
    """
    
    # Format birth details
    dob = child_data.get("dob", "Unknown")
    tob = child_data.get("tob", "12:00 PM") # Default if not provided
    place = f"{child_data.get('city', '')}, {child_data.get('country', '')}"
    name = child_data.get("name", "Child")
    
    prompt = f"""
Generate astrology-based parenting insight for a child using the following birth details:
Date of Birth: {dob}
Birth Time: {tob}
Birth Place: {place}

Determine Sun Sign and Moon Sign first.

Then provide output strictly in JSON format with the following structure:

{{
  "sun_sign": "Hindi Name (English Name)",  e.g., "Simha (Leo)" or "Kumbh (Aquarius)"
  "moon_sign": "Hindi Name (English Name)",
  "core_personality": [
    {{"trait": "Trait Name", "description": "Description "}}
  ],
  "emotional_needs": [
    {{"need": "Need Name", "description": "Description "}}
  ],
  "strengths": [
    {{"strength": "Strength Name", "description": "Description "}}
  ],
  "growth_areas": [
    {{"area": "Area Name", "description": "Description "}}
  ],
  "parenting_tip": {{
    "responsibility": "Give one clear responsibility daily...",
    "appreciation": "...and one moment of appreciation.",
    "balance_advice": "Balance correction with visible praise..."
  }},
  "daily_tasks": [
    {{
      "type": "Discipline Task",
      "title": "Task Name",
      "description": "Task Description",
      "completion_criteria": "Complete if..."
    }},
    {{
      "type": "Responsibility Task",
      "title": "Task Name",
      "description": "Task Description",
      "completion_criteria": "Complete if..."
    }},
    {{
      "type": "Emotional Maturity Task",
      "title": "Task Name",
      "description": "Task Description",
      "completion_criteria": "Complete if..."
    }},
    {{
      "type": "Focus Task",
      "title": "Task Name",
      "description": "Task Description",
      "completion_criteria": "Complete if..."
    }},
    {{
      "type": "Confidence Task",
      "title": "Task Name",
      "description": "Task Description",
      "completion_criteria": "Complete if..."
    }}
  ]
}}

RULES:
1. TARGET AUDIENCE: Indian Parents. Use simple, warm, and respectful English.
2. SUN/MOON SIGNS: Must be in "Hindi Name (English Name)" format.
3. Keep explanations practical and parenting-focused.
4. Avoid complex words. Use simple words that anyone can understand.
5. Keep tone positive, balanced, and actionable.
6. Provide exactly 5 core personality traits, 5 emotional needs, 5 strengths, and 5 growth areas.
7. Provide exactly 5 daily tasks as specified in the types above.
"""

    for _ in range(3):
        try:
            res = ask_llm(prompt)
            cleaned = clean_json_response(res)
            if cleaned:
                data = json.loads(cleaned)
                # Basic validation
                if "sun_sign" in data and "daily_tasks" in data:
                    return data
        except Exception as e:
            print(f"Generation attempt failed: {e}")
            continue
            
    # Fallback structure if generation fails
    return {
        "sun_sign": "Unknown", 
        "moon_sign": "Unknown",
        "core_personality": [{"trait": "Error", "description": "Could not generate report. Please try again."}],
        "emotional_needs": [], "strengths": [], "growth_areas": [],
        "parenting_tip": {"responsibility": "", "appreciation": "", "balance_advice": ""},
        "daily_tasks": []
    }
