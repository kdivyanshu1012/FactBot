import requests
import os

HF_API_KEY = os.getenv("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")
API_URL = "https://api-inference.huggingface.co/models/microsoft/deberta-v3-small-mnli"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def query_hf_model(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

def search_wikipedia(query):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json"
    }
    response = requests.get(url, params=params).json()
    return response.get("query", {}).get("search", [])

def check_fact(statement):
    search_results = search_wikipedia(statement)
    context = search_results[0]["snippet"] if search_results else "No context found."

    payload = {
        "inputs": {
            "premise": context,
            "hypothesis": statement
        }
    }

    output = query_hf_model(payload)

    if isinstance(output, dict) and "error" in output:
        return {
            "status": "error",
            "message": output["error"]
        }

    label_scores = {item["label"]: item["score"] for item in output}
    entailment_score = label_scores.get("ENTAILMENT", 0)

    if entailment_score > 0.7:
        return {
            "status": "true",
            "fact": context.replace("<span class=\"searchmatch\">", "").replace("</span>", ""),
            "confidence": entailment_score,
            "source": "Wikipedia + HuggingFace API"
        }
    else:
        return {
            "status": "false",
            "fact": "This statement might not be factually accurate.",
            "confidence": entailment_score,
            "source": "HuggingFace API"
        }
