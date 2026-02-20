import json
from backend.utils.llm_client import ask_llm, clean_json_response
from backend.prompts import PARENTING_TIPS_PROMPT_TEMPLATE
from backend.schemas import ChildDetails, InsightsOutput, TipsOutput

def generate_parenting_tips_data(child_details: ChildDetails, insights_data: InsightsOutput) -> TipsOutput:
    """
    Generates parenting tips based on personality insights.
    """
    # Format insights for prompt
    traits = ", ".join([t.trait for t in insights_data.core_personality])
    needs = ", ".join([n.need for n in insights_data.emotional_needs])
    strengths = ", ".join([s.strength for s in insights_data.strengths])
    growth = ", ".join([g.area for g in insights_data.growth_areas])
    
    prompt = PARENTING_TIPS_PROMPT_TEMPLATE.format(
        age_years=child_details.age_years if child_details.age_years is not None else "Unknown",
        age_months=child_details.age_months if child_details.age_months is not None else "0",
        personality_traits=traits,
        emotional_needs=needs,
        strengths=strengths,
        growth_areas=growth
    )
    
    for _ in range(3):
        try:
            raw_response = ask_llm(prompt, system_instruction="You are a supportive parenting coach.")
            cleaned_json = clean_json_response(raw_response)
            
            if cleaned_json:
                data = json.loads(cleaned_json)
                return TipsOutput(**data)
        except Exception as e:
            print(f"Tips generation failed (attempt {_}): {e}")
            continue
            
    # Fallback
    return TipsOutput(
        responsibility="Be patient.",
        appreciation="Love your child.",
        balance_advice="Stay calm."
    )
