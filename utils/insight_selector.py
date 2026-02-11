import json
import os
import random

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "insights_database.json")

def get_age_range(age_years):
    if age_years <= 2: return "0-2"
    if age_years <= 5: return "3-5"
    if age_years <= 8: return "6-8"
    if age_years <= 12: return "9-12"
    return "13-16"

def get_birth_time_category(birth_time_str):
    if not birth_time_str or "Skip" in birth_time_str:
        return random.choice(["morning", "afternoon", "evening", "night"])
    
    # Simple parsing of "HH:MM AM/PM"
    try:
        parts = birth_time_str.split()
        time_parts = parts[0].split(":")
        hour = int(time_parts[0])
        period = parts[1].upper()
        
        if period == "PM" and hour != 12:
            hour += 12
        if period == "AM" and hour == 12:
            hour = 0
            
        if 5 <= hour < 12: return "morning"
        if 12 <= hour < 17: return "afternoon"
        if 17 <= hour < 21: return "evening"
        return "night"
    except:
        return random.choice(["morning", "afternoon", "evening", "night"])

def select_insights(child_data):
    """
    Deterministically filters the master database based on child profile.
    Returns 4-6 suggested insights.
    """
    if not os.path.exists(DATABASE_PATH):
        return []

    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
    except:
        return []

    country = child_data.get("country", "India")
    age_range = get_age_range(child_data.get("age_years", 0))
    time_cat = get_birth_time_category(child_data.get("birth_time"))

    # Get insights for country
    country_insights = db.get(country, [])
    if not country_insights:
        # Fallback to India if specific country not found
        country_insights = db.get("India", [])

    # Filter by age and time
    filtered = [
        item for item in country_insights
        if item.get("age_range") == age_range and item.get("birth_time") == time_cat
    ]

    # If too few, broaden by time then age
    if len(filtered) < 4:
        filtered += [
            item for item in country_insights
            if item.get("age_range") == age_range and item not in filtered
        ]
    
    # Shuffle (seed with child data for deterministic but varied results)
    # Note: date objects are not JSON serializable, so we convert them to strings
    seed_str = json.dumps(child_data, sort_keys=True, default=str)
    random.seed(seed_str)
    random.shuffle(filtered)
    
    return filtered[:6] if len(filtered) >= 4 else filtered

def get_available_pool(country, current_selection_ids):
    """
    Returns insights from the country that are NOT in the current selection.
    Used for the "Add Insight" dropdown.
    """
    if not os.path.exists(DATABASE_PATH):
        return []

    try:
        with open(DATABASE_PATH, "r", encoding="utf-8") as f:
            db = json.load(f)
    except:
        return []

    country_insights = db.get(country, db.get("India", []))
    
    pool = [
        item for item in country_insights
        if item.get("id") not in current_selection_ids
    ]
    
    return pool
