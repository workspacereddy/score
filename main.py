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
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
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
    score_element = soup.find("div", class_="cb-col cb-col-100 cb-plyr-tbody cb-rank-hdr cb-lv-main")
    
    if score_element:
        return {"score": score_element.text.strip()}
    
    raise HTTPException(status_code=404, detail="Score not found")

