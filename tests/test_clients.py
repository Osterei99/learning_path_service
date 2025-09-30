import pytest
from app import clients 


class _Capture:
    """Hilfsklasse zum Erfassen von Aufrufen (z.B. der URL, die an get_json gesendet wurde)."""
    def __init__(self):
        self.calls = []


def test_fetch_topics_calls_expected_url(monkeypatch):
    """Testet, ob fetch_topics die korrekte /topics-URL aufruft und die Daten zurückgibt."""
    cap = _Capture()

    def mock_get_json(url):
        cap.calls.append(url)
        return [{"id": "t1", "name": "Topic 1"}]
    
    # monkeypatch.setattr ersetzt die get_json-Funktion in clients
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_topics()
    
    assert response == [{"id": "t1", "name": "Topic 1"}]
    assert len(cap.calls) == 1
    # Prüft, ob die URL mit dem erwarteten Endpunkt endet (z.B. .../api/v1/topics)
    assert cap.calls[0].endswith("/topics")


def test_fetch_skills_calls_expected_url(monkeypatch):
    """Testet, ob fetch_skills die korrekte /skills-URL aufruft und die Daten zurückgibt."""
    cap = _Capture()
    mock_data = [
        {"id": "s1", "skill": "Loops", "topicID": "t1"},
        {"id": "s2", "skill": "Variables", "topicID": "t1"},
    ]

    def mock_get_json(url):
        cap.calls.append(url)
        return mock_data
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_skills()
    
    assert response == mock_data
    assert len(cap.calls) == 1
    # Prüft, ob die URL mit dem erwarteten Endpunkt endet (vom TOPICS_API_BASE_URL)
    assert cap.calls[0].endswith("/skills")


def test_fetch_resources_calls_expected_url_and_converts_id(monkeypatch):
    """
    Testet, ob fetch_resources die korrekte /resources-URL aufruft
    und die Konvertierung von '_id' zu 'id' korrekt durchführt.
    """
    cap = _Capture()
    mock_data_from_api = [
        # Ressource, die bereits 'id' hat
        {"id": "r1", "title": "Resource 1"},
        # Ressource, die nur '_id' hat und konvertiert werden sollte
        {"_id": "60c72b2f6f1d40001a1c4321", "title": "Resource 2"},
    ]
    
    # Die erwartete Ausgabe nach der Konvertierung in fetch_resources
    expected_data = [
        {"id": "r1", "title": "Resource 1"},
        {"_id": "60c72b2f6f1d40001a1c4321", "title": "Resource 2", "id": "60c72b2f6f1d40001a1c4321"},
    ]

    def mock_get_json(url):
        cap.calls.append(url)
        # Wir geben die Daten zurück, wie sie von der API kommen würden
        return mock_data_from_api
    
    monkeypatch.setattr(clients, "get_json", mock_get_json)

    response = clients.fetch_resources()
    
    # Prüft, ob die Daten korrekt umgewandelt wurden
    assert response == expected_data
    assert len(cap.calls) == 1
    # Prüft, ob die URL mit dem erwarteten Endpunkt endet (vom RESOURCES_API_BASE_URL)
    assert cap.calls[0].endswith("/resources")
