import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("LANGFLOW_URL")
ASK_AI_FLOW_ID = os.getenv("ASK_AI_FLOW_ID")
MACRO_FLOW_ID = os.getenv("MACRO_FLOW_ID")
API_KEY = os.getenv("LANGFLOW_API_KEY")

HEADERS = {"x-api-key": API_KEY}

def run_flow(flow_id, input_value):
    response = requests.post(
        f"{BASE_URL}/api/v1/run/{flow_id}",
        json={
            "input_value": input_value,
            "input_type": "text",
            "output_type": "text"
        },
        headers=HEADERS
    )
    data = response.json()
    
    # try main path first
    try:
        return data['outputs'][0]['outputs'][0]['results']['text']['data']['text']
    except (KeyError, IndexError):
        pass
    
    # try alternative path
    try:
        return data['outputs'][0]['outputs'][0]['messages'][0]['message']
    except (KeyError, IndexError):
        pass
    
    # if still failing print raw so we can see
    import json
    print("RAW RESPONSE:")
    print(json.dumps(data, indent=2)[:500])  # first 500 chars only
    return "Could not extract response"

def ask_ai(question, profile, notes):
    full_input = f"""
    Question: {question}
    User Profile: {profile}
    Notes: {notes}
    """
    return run_flow(ASK_AI_FLOW_ID, full_input)

def get_macro(goals, profile):
    full_input = f"""
    Goals: {goals}
    Profile: {profile}
    """
    return run_flow(MACRO_FLOW_ID, full_input)

# # test
# print("Testing Ask AI...")
# print(ask_ai("what should I train today", "25yo, 75kg, intermediate", "did legs yesterday"))

# print("\nTesting Macro Flow...")
# print(get_macro("fat loss", "75kg, 175cm, male"))