import requests
import json
import random

def get_random_paraphrases(text, num_paraphrases=3):
    url = "https://api.ai21.com/studio/v1/paraphrase"

    payload = {
        "style": "formal",
        "text": text
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer XQ6FT29zUsRTW7r4HK1lzJmin6hD7Oee"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        data = json.loads(response.text)
        suggestions = data.get("suggestions", [])
        
        if suggestions:
            # Shuffle the suggestions to make them random
            random.shuffle(suggestions)
            random.shuffle(suggestions)
            return [suggestion["text"] for suggestion in suggestions[:num_paraphrases]]
        else:
            return ["No suggestions found in the response." for _ in range(num_paraphrases)]
    else:
        return [f"Error: {response.status_code} - {response.text}" for _ in range(num_paraphrases)]
