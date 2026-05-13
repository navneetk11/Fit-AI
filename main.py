import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}


def call_groq(system_prompt, user_message):
    """Base function to call Groq API directly."""
    response = requests.post(
        GROQ_URL,
        headers=HEADERS,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.7,
            "max_tokens": 1024
        }
    )
    data = response.json()
    return data['choices'][0]['message']['content']


def ask_ai(question, profile, notes):
    """
    Ask AI coach a fitness question.
    Uses user profile and notes for personalized response.
    Routes math questions to calculator logic.
    """
    # check if math question first
    router_prompt = """You are a decision-making assistant.
    If the user is asking to calculate a specific math 
    expression with actual numbers like '2+2' or '150*4', 
    respond with exactly 'MATH'.
    For all fitness, nutrition, workout, or advice questions, 
    respond with exactly 'ADVICE'.
    Respond with ONE word only."""

    route = call_groq(router_prompt, question).strip().upper()

    if "MATH" in route:
        # handle as math
        math_prompt = """You are a calculator assistant. 
        Evaluate the mathematical expression and return 
        just the numerical answer."""
        return call_groq(math_prompt, question)

    else:
        # handle as fitness advice
        system_prompt = f"""You are an expert personal fitness 
coach and nutritionist. You provide personalized, practical 
advice based on the user's profile and recent activity.

User Profile:
{profile}

Recent Notes:
{notes}

Guidelines:
- Give specific, actionable advice
- Reference the user's profile details in your response
- Keep responses focused and practical
- Use the notes to make responses contextual
- Be encouraging and motivational"""

        return call_groq(system_prompt, question)


def get_macro(goals, profile):
    """
    Calculate personalized macros based on goals and profile.
    Returns JSON with protein, carbs, fat, calories.
    """
    system_prompt = """You are an expert sports nutritionist.
Calculate personalized daily macro targets based on the 
user's profile and goals.

You MUST respond with ONLY a JSON object in this exact format,
nothing else, no explanation, no markdown:
{"protein": 150, "carbs": 200, "fat": 55, "calories": 1900}

Calculate based on:
- BMR using Mifflin-St Jeor formula
- Activity multiplier from activity level
- Goal adjustment (deficit for fat loss, surplus for muscle)
- Protein: 1.6-2.2g per kg bodyweight
- Fat: 20-35% of total calories
- Carbs: remaining calories"""

    user_message = f"""
Goals and Preferences:
{goals}

User Profile:
{profile}

Calculate my daily macro targets and return ONLY the JSON.
"""

    result = call_groq(system_prompt, user_message)

    # clean up response in case model adds extra text
    import re
    json_match = re.search(r'\{.*?\}', result, re.DOTALL)
    if json_match:
        return json_match.group()
    return result


# ── TEST ─────────────────────────────────────────────────
if __name__ == "__main__":
    print("Testing ask_ai...")
    response = ask_ai(
        question="What should I train today?",
        profile="Age: 25, Weight: 70kg, Goal: Build Muscle, Experience: Intermediate",
        notes="Did legs yesterday"
    )
    print("Ask AI:", response[:200])

    print("\nTesting get_macro...")
    macros = get_macro(
        goals="Goal: Build Muscle, Activity: Moderately Active",
        profile="Age: 25, Gender: Female, Weight: 70kg, Height: 165cm"
    )
    print("Macros:", macros)