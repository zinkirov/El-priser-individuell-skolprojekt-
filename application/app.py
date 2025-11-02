from flask import Flask, render_template, request, make_response
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
app = Flask(__name__)

def validate_date(year, month, day):
    """
    Validerar att ett datum ligger mellan 2022-11-01 och imorgon.
    Returnerar True om giltigt, annars False.
    Denna funktion används för TDD-exempel.
    """
    try:
        datum = datetime(year, month, day)
        min_datum = datetime(2022, 11, 1)
        max_datum = datetime.now() + timedelta(days=1)
        return min_datum <= datum <= max_datum
    except ValueError:
        return False

@app.errorhandler(404)
def page_not_found(e):
    """Visar en anpassad 404-sida om användaren går till en ogiltig URL"""

    return render_template('404.html'), 404

@app.route("/")
def index():
    """Visar formulärsidan där användaren kan välja datum och område"""

    return render_template("index.html", now=datetime.now(), bakgrundsklass="start-bakgrund")

@app.route("/form")
def form():
    """Visar formulärsidan där användaren kan välja datum och område"""
    
    return render_template("form.html", now=datetime.now(), bakgrundsklass="start-bakgrund")

@app.post("/api")
def api_post():
    """Tar emot formulärdata, validerar datum och hämtar elpriser från API"""
    try:
        # Plocka argumenten från request.form som är en
        # ImmitableMultiDict, dvs kan läsas som en vanlig dictionary
        år = request.form["år"]
        månad = request.form["månad"]
        dag = request.form["dag"]
        prisklass = request.form["prisklass"]

        #Skapa datumobjekt från formulärdata
        datum_str = f"{år}-{månad}-{dag}"
        datum = datetime.strptime(datum_str, "%Y-%m-%d")
        
        # Om datumet är giltigt, fortsätter med API-anrop
        if not validate_date(int(år), int(månad), int(dag)):
            felmeddelande = "Datumet måste vara mellan 2022-11-01 och imorgon."
            return render_template("form.html", fel=felmeddelande, now=datetime.now(),
                           år=år, månad=månad, dag=dag, prisklass=prisklass)   
       
        data_url = f"https://www.elprisetjustnu.se/api/v1/prices/{år}/{månad}-{dag}_{prisklass}.json"
        json_data = requests.get(data_url)
        # Tolka JSON-svaret
        data = json.loads(json_data.text)
        # Konvertera till DataFrame
        df = pd.DataFrame(data)
        df["time_start"] = pd.to_datetime(df["time_start"]).dt.strftime("%H:%M")
        df["time_end"] = pd.to_datetime(df["time_end"]).dt.strftime("%H:%M")

        # Skapa HTML-tabell med utvalda kolumner
        table_data = df.to_html(
            columns=["SEK_per_kWh", "EUR_per_kWh", "EXR", "time_start", "time_end"],
            classes="table p-5",
            justify="left"
        )
        # Skapar svar med cookies
        response = make_response(render_template(
        "result.html",
        data=table_data,
         datum=datum_str,
        område=prisklass,
        now=datetime.now(),
        bakgrundsklass="api-bakgrund"

        ))
        response.set_cookie("år", år)
        response.set_cookie("månad", månad)
        response.set_cookie("dag", dag)
        response.set_cookie("prisklass", prisklass)
        return response

    except Exception as e:
        felmeddelande = "Kunde inte hämta data.Kontrollera att datum och prisklass är giltiga."
        return render_template("form.html", fel=felmeddelande, now=datetime.now())
    

if __name__ == "__main__":
    app.run()




