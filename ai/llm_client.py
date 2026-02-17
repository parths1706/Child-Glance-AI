import os
import requests
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
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("!!! LLM ERROR: OPENROUTER_API_KEY not found in environment variables.")
        return ""

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/parths1706/Child-Glance-AI", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "Parenting Guide AI", # Optional. Shows in rankings on openrouter.ai.
    }
    
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        
        json_response = response.json()
        
        # Parse OpenAI-compatible response
        if "choices" in json_response and len(json_response["choices"]) > 0:
            return json_response["choices"][0]["message"]["content"].strip()
        else:
            print(f"!!! LLM ERROR: Unexpected response format: {json_response}")
            return ""

    except requests.exceptions.RequestException as e:
        print(f"!!! LLM NETWORK ERROR: {e}")
        return ""
    except Exception as e:
        print(f"!!! LLM ERROR: {e}")
        return ""
