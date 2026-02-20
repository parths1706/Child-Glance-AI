import json
from backend.utils.llm_client import ask_llm, clean_json_response
from backend.prompts import DAILY_TASKS_PROMPT_TEMPLATE
from backend.schemas import ChildDetails, TipsOutput, TasksOutput

def generate_tasks_data(child_details: ChildDetails, tips_data: TipsOutput) -> TasksOutput:
    """
    Generates daily tasks based on parenting tips and age.
    """
    prompt = DAILY_TASKS_PROMPT_TEMPLATE.format(
        age_years=child_details.age_years if child_details.age_years is not None else "Unknown",
        age_months=child_details.age_months if child_details.age_months is not None else "0",
        responsibility_tip=tips_data.responsibility,
        appreciation_tip=tips_data.appreciation,
        balance_tip=tips_data.balance_advice
    )
    
    for _ in range(3):
        try:
            raw_response = ask_llm(prompt, system_instruction="You are a child development expert specializing in Indian parenting and behavioral psychology.")
            cleaned_json = clean_json_response(raw_response)
            
            if cleaned_json:
                data = json.loads(cleaned_json)
                return TasksOutput(**data)
        except Exception as e:
            print(f"Tasks generation failed (attempt {_}): {e}")
            continue
            
    # Fallback
    return TasksOutput(daily_tasks=[])
