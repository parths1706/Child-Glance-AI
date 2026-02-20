import requests
import streamlit as st
import time

API_BASE_URL = "http://localhost:8001/api/v1"

def post_to_api(endpoint: str, payload: dict, max_retries=3):
    """
    Helper function to POST to the backend API with retries and error handling.
    """
    url = f"{API_BASE_URL}/{endpoint}"
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            st.error("Server timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to server. Is the backend running?")
            return None
        
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None
            
    return None

def fetch_astrology(child_details):
    payload = {"child_details": child_details}
    return post_to_api("generate-astrology", payload)

def fetch_insights(child_details, astrology_output):
    payload = {
        "child_details": child_details,
        "astrology_output": astrology_output
    }
    return post_to_api("generate-insights", payload)

def fetch_parenting_tips(child_details, insights_output):
    payload = {
        "child_details": child_details,
        "insights_output": insights_output
    }
    return post_to_api("generate-parenting-tips", payload)

def fetch_daily_tasks(child_details, tips_output):
    payload = {
        "child_details": child_details,
        "tips_output": tips_output
    }
    return post_to_api("generate-daily-tasks", payload)
