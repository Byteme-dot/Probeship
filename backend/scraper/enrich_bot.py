import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import quote
from dotenv import load_dotenv
from pathlib import Path
import os


# ---------------- LOAD ENV ----------------

env_path = (
    Path(__file__)
    .resolve()
    .parent.parent / ".env"
)

load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("SCRAPER_API_KEY")


async def enrich_single_internship(link):

    try:

        encoded_url = quote(link)

        proxy_url = (

            f"http://api.scraperapi.com"

            f"?api_key={API_KEY}"

            f"&url={encoded_url}"

        )

        timeout = aiohttp.ClientTimeout(
            total=10
        )

        async with aiohttp.ClientSession(
            timeout=timeout
        ) as session:

            async with session.get(
                proxy_url
            ) as response:

                html = await response.text()

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # ---------------- SKILLS ----------------

        skills_tags = soup.select(
            ".round_tabs"
        )

        skills = ", ".join([

            s.get_text(strip=True)

            for s in skills_tags

        ])

        return {

            "Skills": skills,
            "Link": link

        }

    except Exception as e:

        print(
            f"Enrichment failed: {e}"
        )

        return {

            "Skills": "",
            "Link": link

        }