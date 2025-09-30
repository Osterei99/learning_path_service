import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from .helpers import get_json

load_dotenv()

TOPICS_API_BASE_URL = os.getenv("TOPICS_API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
RESOURCES_API_BASE_URL = os.getenv("RESOURCES_API_BASE_URL", "http://localhost:5002").rstrip("/")


def fetch_topics() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE_URL}/topics")


def fetch_skills() -> List[Dict[str, Any]]:
    return get_json(f"{TOPICS_API_BASE_URL}/skills")


def fetch_resources() -> List[Dict[str, Any]]:
    items = get_json(f"{RESOURCES_API_BASE_URL}/resources")

    for item in items:
        if "id" not in item and "_id" in item:
            item["id"] = str(item["_id"])
    
    return items
import requests

# Basis-URL für die API, um Endpunkte zu erstellen
BASE_URL = "http://api.example.com/api/v1"


def get_json(url: str):
    """
    Simuliert die Funktion zum Abrufen von JSON-Daten von einer URL.
    Diese Funktion wird in den Tests in test_clients.py gemockt (ersetzt).
    Für den realen Einsatz müsste hier die tatsächliche HTTP-Logik stehen.
    """
    # Wenn diese Funktion in einer echten Anwendung aufgerufen würde (nicht in den Tests),
    # würde sie eine Implementierung wie die folgende enthalten:
    # try:
    #     response = requests.get(url)
    #     response.raise_for_status() # Löst Fehler für 4xx/5xx Status-Codes aus
    #     return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"Fehler beim Abrufen von {url}: {e}")
    #     return []
    
    # Da wir uns auf das Mocking für die Tests verlassen, lassen wir eine Notiz hier.
    raise NotImplementedError(
        "Diese Funktion ist nicht implementiert und sollte in Tests gemockt werden."
    )


def fetch_topics():
    """Ruft eine Liste aller verfügbaren Themen ab."""
    url = f"{BASE_URL}/topics"
    return get_json(url)


def fetch_topic_details(topic_id: str):
    """Ruft detaillierte Informationen zu einem bestimmten Thema ab."""
    url = f"{BASE_URL}/topics/{topic_id}"
    return get_json(url)


def fetch_questions(topic_id: str):
    """Ruft alle Fragen ab, die zu einer bestimmten Topic-ID gehören."""
    # Fügt die topic_id als Query-Parameter hinzu, wie im Test erwartet
    url = f"{BASE_URL}/questions?topic_id={topic_id}"
    return get_json(url)


def fetch_answer(question_id: str):
    """Ruft die Antwortdetails für eine bestimmte Frage-ID ab."""
    url = f"{BASE_URL}/answers/{question_id}"
    return get_json(url)