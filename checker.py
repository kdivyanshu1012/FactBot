
import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

def check_fact(fact):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }
    api_url = "https://api-inference.huggingface.co/models/ynie/bart-large-snli_mnli"

    response = requests.post(api_url, headers=headers, json={"inputs": {
        "premise": "This is a factual claim.",
        "hypothesis": fact
    }})
    if response.status_code != 200:
        return "AI check failed. Please try again later."

    result = response.json()
    label = result[0]['label']
    if label == "ENTAILMENT":
        return "✅ This statement is likely factual."
    elif label == "CONTRADICTION":
        return "❌ This seems to be incorrect."
    else:
        return "🤔 Not sure about this. Needs further verification."
