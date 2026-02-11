import json
import os
import time
from ai.llm_client import ask_llm

COUNTRIES = ["India", "USA", "Germany", "UK", "Canada", "Australia"]
AGE_RANGES = ["0-2", "3-5", "6-8", "9-12", "13-16"]
BIRTH_TIMES = ["morning", "afternoon", "evening", "night"]

def clean_json_response(raw_response):
    if not raw_response:
        return None
    if "```json" in raw_response:
        raw_response = raw_response.split("```json")[1].split("```")[0]
    elif "```" in raw_response:
        raw_response = raw_response.split("```")[1].split("```")[0]
    return raw_response.strip()

def generate_insights_for_country(country):
    print(f"🚀 Generating insights for {country}...")
    all_insights = []
    
    for age in AGE_RANGES:
        for b_time in BIRTH_TIMES:
            print(f"  - Working on {age} years ({b_time})...")
            
            prompt = f"""
            You are a child development expert. Generate 5 unique, 1-line personality insights for a child.
            
            STRICT CONTEXT:
            - Country: {country}
            - Age: {age} years
            - Birth Time: {b_time}
            
            RULES:
            - Description must be EXACTLY 1 sentence (max 15 words).
            - Professional, realistic, and practical.
            - Format: JSON list only.

            JSON STRUCTURE:
            [
              {{
                "id": "{country[:3].upper()}_{age.replace('-', '')}_{b_time[:1]}_{{i}}",
                "category": "SOCIAL/EMOTIONAL/COGNITIVE",
                "title": "Short Title",
                "description": "Exactly one line of insight.",
                "source": "behavioral_observation",
                "age_range": "{age}",
                "birth_time": "{b_time}"
              }}
            ]
            """
            
            retries = 3
            success = False
            while retries > 0 and not success:
                try:
                    raw = ask_llm(prompt)
                    cleaned = clean_json_response(raw)
                    if cleaned:
                        insights = json.loads(cleaned)
                        for item in insights:
                            item["country"] = country
                        all_insights.extend(insights)
                        print(f"    ✅ Added {len(insights)} insights.")
                        success = True
                    else:
                        print(f"    ⚠️ Empty response for {age} ({b_time}).")
                        retries -= 1
                except Exception as e:
                    print(f"    ❌ Attempt failed for {age} ({b_time}): {e}")
                    retries -= 1
                
                if not success:
                    time.sleep(3) # Wait before retry or next attempt
            
            time.sleep(1) # Extra gap between categories
                    
            if not success:
                print(f"    ⚠️ Failed to generate for {age} ({b_time}) after retries.")
                
    return all_insights

def run_generator():
    output_path = "/home/iinx-user/Parenting_Guide/data/insights_database.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load existing to resume if needed
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            try:
                master_db = json.load(f)
            except:
                master_db = {}
    else:
        master_db = {}
    
    for country in COUNTRIES:
        # Skip if already has data (optional, but good for resuming)
        if master_db.get(country):
            print(f"⏩ {country} already has data. Skipping...")
            continue
            
        master_db[country] = generate_insights_for_country(country)
        
        # Save after each country
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(master_db, f, indent=2)
        print(f"📂 Progress saved for {country}.")
    
    print(f"\n✨ SUCCESS: Master database complete at {output_path}")

if __name__ == "__main__":
    run_generator()
