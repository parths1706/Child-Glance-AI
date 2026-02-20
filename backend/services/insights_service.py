import json
from backend.utils.llm_client import ask_llm, clean_json_response
from backend.prompts import INSIGHTS_PROMPT_TEMPLATE
from backend.schemas import ChildDetails, AstrologyOutput, InsightsOutput

def generate_insights_data(child_details: ChildDetails, astrology_data: AstrologyOutput) -> InsightsOutput:
    """
    Generates personality insights based on astrology data.
    """
    prompt = INSIGHTS_PROMPT_TEMPLATE.format(
        dob=child_details.dob,
        sun_sign=astrology_data.sun_sign,
        moon_sign=astrology_data.moon_sign
    )
    
    for _ in range(3):
        try:
            raw_response = ask_llm(prompt, system_instruction="You are a child psychologist and astrologer.")
            cleaned_json = clean_json_response(raw_response)
            
            if cleaned_json:
                data = json.loads(cleaned_json)
                return InsightsOutput(**data)
        except Exception as e:
            print(f"Insights generation failed (attempt {_}): {e}")
            continue
            
    # Fallback
    return InsightsOutput(
        core_personality=[],
        emotional_needs=[],
        strengths=[],
        growth_areas=[]
    )
