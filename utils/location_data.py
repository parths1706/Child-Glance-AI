import json
import pycountry
import os
import requests

def get_all_countries():
    # Returns a list of all country names
    return sorted([country.name for country in pycountry.countries])

def get_visitor_country():
    """Attempts to detect visitor country via IP. Returns country name or None."""
    try:
        # Use ip-api.com (free, no key needed for simple usage)
        response = requests.get("http://ip-api.com/json/", timeout=2)
        if response.status_code == 200:
            data = response.json()
            country_code = data.get("countryCode")
            if country_code:
                country = pycountry.countries.get(alpha_2=country_code)
                return country.name if country else None
    except Exception:
        pass
    return None

def get_cities_by_country(country_name):
    """Fetches all cities for a given country from a global API."""
    try:
        # Use countriesnow.space API (Free, no key needed)
        url = "https://countriesnow.space/api/v0.1/countries/cities"
        response = requests.post(url, json={"country": country_name}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if not data.get("error"):
                return data.get("data", [])
    except Exception:
        pass
    
    # Fallback to local data if API fails
    local_data = load_city_data()
    return local_data.get(country_name, [])

def load_city_data():
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "world_cities.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}