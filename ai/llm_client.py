import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def clean_json_response(raw_response):
    if not raw_response:
        return ""
    
    # 1. Try markdown blocks first
    if "```json" in raw_response:
        raw_response = raw_response.split("```json")[1].split("```")[0]
    elif "```" in raw_response:
        raw_response = raw_response.split("```")[1].split("```")[0]
    
    # 2. If no backticks, try to find the list/object boundaries
    raw_response = raw_response.strip()
    if not (raw_response.startswith('[') or raw_response.startswith('{')):
        # Look for the first '[' and last ']'
        start = raw_response.find('[')
        end = raw_response.rfind(']')
        if start != -1 and end != -1:
            raw_response = raw_response[start:end+1]
            
    return raw_response.strip()

def ask_llm(prompt: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return ""

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"!!! LLM ERROR: {e}")
        return ""
