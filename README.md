## Elpriset Just Nu

Ett Flask-projekt som visar aktuella elpriser i Sverige baserat på datum och prisklass (SE1–SE4).  
Användaren kan välja datum och område via ett formulär, varpå appen hämtar data från det öppna API:t [elprisetjustnu.se](https://www.elprisetjustnu.se).

---

## Projektstruktur
project-root/
├── application/
│   ├── __init__.py
│   ├── app.py
│   ├── data/            
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── images/
│   │   └── js/
│   ├── templates/
│   │   ├── 404.html
│   │   ├── footer.html
│   │   ├── form.html
│   │   ├── header.html
│   │   ├── layout.html
│   │   ├── index.html
├── tests/
│   ├── __init__.py
│   ├── test_app.py
│   └── test_validation.py
├── docs/                
├── requirements.txt         
└── README.md    

## Installation

1. **Skapa och aktivera ett virtuellt Python-miljö:**
   python -m venv venv
   source venv/bin/activate     # macOS/Linux
   venv\Scripts\activate        # Windows

2. **Installera beroenden:**

pip install -r requirements.txt
Om du inte har en requirements.txt, skapa en med:
pip install flask requests pandas pytest
pip freeze > requirements.txt

## Kör Flask-appen
Gå till mappen där app.py ligger (application/) och kör:
flask --app app run --debug
Appen körs på http://127.0.0.1:5000/

## Funktioner

- Hämtar elpriser från API:t https://www.elprisetjustnu.se
- Validerar datum mellan 2022-11-01 och imorgon
- Använder cookies för att spara senaste val
- Visar tabell med elprisdata i SEK/EUR per timme
- Hanterar 404-fel med egen sida

## Testning (TDD)

- Testar att startsida och formulärsida laddas korrekt
- Testar att formulär innehåller alla fält
- Testar datumvalidering via TDD-funktion (validate_date)

## Kör alla tester
pytest -v

## Länkar
API: https://www.elprisetjustnu.se/elpris-api
GitHub: https://github.com/zinkirov
