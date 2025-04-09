from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live-score")
def get_score():
    url = "https://www.livescore.com/en/football/champions-league/knockout-round-play-offs/arsenal-vs-real-madrid/1461442/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching the data from live sport site")

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the HTML element that contains the score (you need to inspect the site manually)
    score_element = soup.find("div", class_="ti")
    
    if score_element:
        return {"score": score_element.text.strip()}
    
    raise HTTPException(status_code=404, detail="Score not found")

