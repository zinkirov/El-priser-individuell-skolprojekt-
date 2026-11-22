import json
from unittest.mock import Mock

import pytest
import requests

from application.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Testar att startsidan laddas korrekt"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Elpriset Just Nu" in response.data

def test_form_page(client):
    """Testar att formulärsidan laddas korrekt"""
    response = client.get("/form")
    assert response.status_code == 200
    assert "Välj datum och prisklass" in response.data.decode("utf-8")

def test_form_html_fields(client):
    """Testar att formulärsidan innehåller alla fält"""
    response = client.get("/form")
    html = response.data.decode("utf-8")
    assert response.status_code == 200
    assert 'name="år"' in html
    assert 'name="månad"' in html
    assert 'name="dag"' in html
    assert 'name="prisklass"' in html
    assert "<select" in html
    assert "<form" in html

def test_404_page(client):
    """Testar att 404-sidan visas korrekt"""
    response = client.get("/dennasidafinnsinte")
    html = response.data.decode("utf-8")
    assert response.status_code == 404
    assert "Sidan du söker finns inte" in html    

def test_form_submission_displays_prices(client, monkeypatch):
    price_data = [
        {
            "SEK_per_kWh": 1.2345,
            "EUR_per_kWh": 0.1111,
            "EXR": 11.1111,
            "time_start": "2025-01-15T00:00:00+01:00",
            "time_end": "2025-01-15T01:00:00+01:00",
        }
    ]

    fake_response = Mock()
    fake_response.text = json.dumps(price_data)

    fake_get = Mock(return_value=fake_response)
    monkeypatch.setattr("application.app.requests.get", fake_get)

    response = client.post(
        "/api",
        data={
            "år": "2025",
            "månad": "01",
            "dag": "15",
            "prisklass": "SE3",
        },
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Elpriser för 2025-01-15 i område SE3" in html
    assert "<table" in html
    assert "1.2345" in html
    assert "00:00" in html
    assert "01:00" in html

    fake_get.assert_called_once_with(
        "https://www.elprisetjustnu.se/api/v1/prices/2025/01-15_SE3.json"
    )

def test_form_rejects_old_date_without_fetching_prices(client, monkeypatch):
    fake_get = Mock()
    monkeypatch.setattr("application.app.requests.get", fake_get)

    response = client.post(
        "/api",
        data={
            "år": "2020",
            "månad": "01",
            "dag": "15",
            "prisklass": "SE3",
        },
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Datumet måste vara mellan 2022-11-01 och imorgon." in html
    assert "<table" not in html

    fake_get.assert_not_called()

def test_form_handles_price_service_connection_error(client, monkeypatch):
    fake_get = Mock(
        side_effect=requests.exceptions.ConnectionError(
            "Pristjänsten kan inte nås"
        )
    )
    monkeypatch.setattr("application.app.requests.get", fake_get)

    response = client.post(
        "/api",
        data={
            "år": "2025",
            "månad": "01",
            "dag": "15",
            "prisklass": "SE3",
        },
    )

    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Kunde inte hämta data." in html
    assert "<table" not in html

    fake_get.assert_called_once()

def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}