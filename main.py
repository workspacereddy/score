# main.py
from fastapi import FastAPI
from bs4 import BeautifulSoup
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["https://your-vercel-app.vercel.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/live-score")
def get_score():
    url = "https://www.livesport.com/en/match/soccer/UZYB9WPh/#/match-summary/match-summary"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the HTML element that contains the score (you need to inspect the site manually)
    score_element = soup.find("div", class="detailScore__wrapper")  # Example
    if score_element:
        return {"score": score_element.text.strip()}
    return {"score": "Score not found"}
