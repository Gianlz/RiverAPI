from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from fastapi.responses import JSONResponse
from lxml import html
import aiohttp

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500", 
    "https://gianlz.github.io/RiverTracker/",
    "https://gianlz.github.io",
    "https://gianlz.github.io/"
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_river_height():
    url = 'https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            height = tree.xpath('/html/body/div/div/section[2]/section/div[1]/div/div/div[2]/div/div/div/div/table/tbody/tr[1]/td[2]/text()')
            if height:
                return height[0].strip()  
            else:
                return None
        else:
            return None
    except requests.exceptions.RequestException:
        return None

@app.get('/api/river-height', response_class=JSONResponse)
async def get_river_height():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://defesacivil.riodosul.sc.gov.br/index.php?r=externo%2Fmetragem') as response:
            if response.status == 200:
                tree = html.fromstring(await response.content.read())
                height = tree.xpath('//td[2]/text()')[0].strip()
                return {'height': height}
    raise HTTPException(status_code=500, detail='Failed to fetch river height')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
