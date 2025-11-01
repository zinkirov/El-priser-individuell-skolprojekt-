import pytest
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


