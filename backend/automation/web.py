import webbrowser
import requests
from datetime import datetime

def open_website(url: str):
    webbrowser.open(url)

def search_youtube(query: str):
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

def get_motivational_quote() -> str:
    try:
        r = requests.get("https://zenquotes.io/api/random")
        if r.status_code == 200:
            return r.json()[0]["q"]
    except:
        pass
    return "Stay positive and keep pushing forward."

def get_news(api_key: str) -> list:
    try:
        headers = {'Authorization': f'Bearer {api_key}'}
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us", headers=headers)
        if r.status_code == 200:
            data = r.json()
            return [article['title'] for article in data.get('articles', [])[:3]]
    except:
        pass
    return ["Could not fetch the news at this time."]

def define_word(word: str) -> str:
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if res.status_code == 200:
            data = res.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
    except:
        pass
    return "Sorry, I couldn't find the definition."

def get_weather() -> str:
    return "Weather API not integrated. Replace with your own."
