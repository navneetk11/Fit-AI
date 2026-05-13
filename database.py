import os
from datetime import datetime
from dotenv import load_dotenv
from astrapy import DataAPIClient
from functools import lru_cache
import concurrent.futures

load_dotenv()

# ── CACHED CONNECTION ────────────────────────────────────
# connection is created once and reused — saves 1-2 seconds
@lru_cache(maxsize=1)
def get_db():
    client = DataAPIClient(os.getenv("ASTRA_DB_TOKEN"))
    db = client.get_database_by_api_endpoint(
        os.getenv("ASTRA_DB_ENDPOINT")
    )
    return db

@lru_cache(maxsize=1)
def get_collections():
    db = get_db()
    try:
        users = db.create_collection("users")
    except:
        users = db.get_collection("users")
    try:
        workouts = db.create_collection("workouts")
    except:
        workouts = db.get_collection("workouts")
    try:
        notes = db.create_collection("notes")
    except:
        notes = db.get_collection("notes")
    try:
        reminders = db.create_collection("reminders")
    except:
        reminders = db.get_collection("reminders")
    return users, workouts, notes, reminders

# ── USER PROFILE ─────────────────────────────────────────
def save_profile(email, profile_data):
    users, _, _, _ = get_collections()
    users.find_one_and_replace(
        {"email": email},
        {
            "email": email,
            "name": profile_data.get("name"),
            "age": profile_data.get("age"),
            "weight": profile_data.get("weight"),
            "height": profile_data.get("height"),
            "gender": profile_data.get("gender"),
            "goal": profile_data.get("goal"),
            "experience": profile_data.get("experience"),
            "equipment": profile_data.get("equipment", []),
            "updated_at": datetime.now().isoformat()
        },
        upsert=True
    )

def load_profile(email):
    users, _, _, _ = get_collections()
    result = users.find_one({"email": email})
    if result:
        result = dict(result)
        result.pop("_id", None)
        result.pop("updated_at", None)
        return result
    return None

# ── WORKOUT LOG ───────────────────────────────────────────
def save_workout(email, workout_data):
    _, workouts, _, _ = get_collections()
    workouts.insert_one({
        "email": email,
        "date": workout_data.get("date"),
        "type": workout_data.get("type"),
        "duration": workout_data.get("duration"),
        "notes": workout_data.get("notes"),
        "created_at": datetime.now().isoformat()
    })

def load_workouts(email):
    _, workouts, _, _ = get_collections()
    results = workouts.find({"email": email})
    workout_list = []
    for w in results:
        workout_list.append({
            "date": w.get("date"),
            "type": w.get("type"),
            "duration": w.get("duration"),
            "notes": w.get("notes")
        })
    return workout_list

# ── NOTES ─────────────────────────────────────────────────
def save_notes(email, notes_text):
    _, _, notes, _ = get_collections()
    notes.find_one_and_replace(
        {"email": email},
        {
            "email": email,
            "notes": notes_text,
            "updated_at": datetime.now().isoformat()
        },
        upsert=True
    )

def load_notes(email):
    _, _, notes, _ = get_collections()
    result = notes.find_one({"email": email})
    return result.get("notes", "") if result else ""

# ── REMINDERS ─────────────────────────────────────────────
def save_reminder_settings(email, settings):
    _, _, _, reminders = get_collections()
    reminders.find_one_and_replace(
        {"email": email},
        {
            "email": email,
            "days": settings.get("days", []),
            "time": settings.get("time"),
            "active": True,
            "updated_at": datetime.now().isoformat()
        },
        upsert=True
    )

def load_reminder_settings(email):
    _, _, _, reminders = get_collections()
    result = reminders.find_one({"email": email})
    if result:
        result = dict(result)
        result.pop("_id", None)
        result.pop("updated_at", None)
        return result
    return {}

# ── LOAD ALL USER DATA IN PARALLEL ───────────────────────
# this is the key function — loads everything at once
# instead of 4 separate sequential calls
def load_all_user_data(email):
    def fetch_profile():
        return load_profile(email)

    def fetch_workouts():
        return load_workouts(email)

    def fetch_notes():
        return load_notes(email)

    def fetch_reminders():
        return load_reminder_settings(email)

    # run all 4 calls at the same time
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_profile = executor.submit(fetch_profile)
        future_workouts = executor.submit(fetch_workouts)
        future_notes = executor.submit(fetch_notes)
        future_reminders = executor.submit(fetch_reminders)

        profile = future_profile.result()
        workouts = future_workouts.result()
        notes = future_notes.result()
        reminders = future_reminders.result()

    return profile, workouts, notes, reminders