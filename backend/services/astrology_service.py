import json
from backend.utils.llm_client import ask_llm, clean_json_response
from backend.prompts import ASTROLOGY_PROMPT_TEMPLATE
from backend.schemas import ChildDetails, AstrologyOutput

def generate_astrology_data(child_details: ChildDetails) -> AstrologyOutput:
    """
    Generates astrology details (Sun Sign, Moon Sign) based on birth data.
    """
    prompt = ASTROLOGY_PROMPT_TEMPLATE.format(
        dob=child_details.dob,
        tob=child_details.tob,
        place=f"{child_details.city}, {child_details.country}"
    )
    
    for _ in range(3): # Retry logic
        try:
            raw_response = ask_llm(prompt, system_instruction="You are an expert Vedic Astrologer.")
            cleaned_json = clean_json_response(raw_response)
            
            if cleaned_json:
                data = json.loads(cleaned_json)
                return AstrologyOutput(**data)
        except Exception as e:
            print(f"Astrology generation failed (attempt {_}): {e}")
            continue
            
    # Fallback
    return AstrologyOutput(
        sun_sign="Unknown (Unknown)",
        moon_sign="Unknown (Unknown)"
    )
