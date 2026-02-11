def safe_text(response, fallback):
    if not response or not response.strip():
        return fallback
    return response
