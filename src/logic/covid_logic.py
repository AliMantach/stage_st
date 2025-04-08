import requests

def get_covid_stats(country):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{country}?strict=true"
        r = requests.get(url)
        d = r.json()
        return {
            "cases": d["cases"],
            "deaths": d["deaths"],
            "recovered": d["recovered"]
        }
    except Exception:
        return None