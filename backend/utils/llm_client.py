import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Centralized Configuration
LLM_CONFIG = {
    "model": "deepseek/deepseek-chat",
    "temperature": 0.7,
    "max_tokens": 2000,
    "top_p": 1.0,
}

def clean_json_response(raw_response: str) -> str:
    """
    Cleans the LLM response to extract valid JSON.
    """
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
        # Look for the first '[' or '{' and last ']' or '}'
        start_brace = raw_response.find('{')
        start_bracket = raw_response.find('[')
        
        start = -1
        if start_brace != -1 and start_bracket != -1:
            start = min(start_brace, start_bracket)
        elif start_brace != -1:
            start = start_brace
        elif start_bracket != -1:
            start = start_bracket
            
        end_brace = raw_response.rfind('}')
        end_bracket = raw_response.rfind(']')
        
        end = -1
        if end_brace != -1 and end_bracket != -1:
            end = max(end_brace, end_bracket)
        elif end_brace != -1:
            end = end_brace
        elif end_bracket != -1:
            end = end_bracket
            
        if start != -1 and end != -1:
            raw_response = raw_response[start:end+1]
            
    return raw_response.strip()

def ask_llm(prompt: str, system_instruction: str = "You are a helpful parenting assistant.") -> str:
    """
    Makes a request to the LLM with consistent settings.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        print("!!! LLM ERROR: OPENROUTER_API_KEY not found.")
        return ""

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/parths1706/Child-Glance-AI",
        "X-Title": "Parenting Guide AI",
    }
    
    data = {
        "model": LLM_CONFIG["model"],
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        "temperature": LLM_CONFIG["temperature"],
        "max_tokens": LLM_CONFIG["max_tokens"],
        "top_p": LLM_CONFIG["top_p"],
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        response.raise_for_status()
        
        json_response = response.json()
        
        if "choices" in json_response and len(json_response["choices"]) > 0:
            content = json_response["choices"][0]["message"]["content"].strip()
            return content
        else:
            print(f"!!! LLM ERROR: Unexpected response format: {json_response}")
            return ""

    except requests.exceptions.RequestException as e:
        print(f"!!! LLM NETWORK ERROR: {e}")
        return ""
    except Exception as e:
        print(f"!!! LLM ERROR: {e}")
        return ""
