import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import quote
from dotenv import load_dotenv
from pathlib import Path
import os
import re

env_path = (
    Path(__file__)
    .resolve()
    .parent.parent / ".env"
)

load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("SCRAPER_API_KEY")


async def get_internships_pro(search_query):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True
        )

        try:

            context = await browser.new_context()

            page = await context.new_page()

            target_url = (
                f"https://internshala.com/"
                f"internships/keywords-{search_query}"
            )

            encoded_url = quote(target_url)

            proxy_url = (
                f"http://api.scraperapi.com"
                f"?api_key={API_KEY}"
                f"&url={encoded_url}"
                f"&country_code=in"
            )

            print(
                f"Protected Search: {search_query}"
            )

            await page.goto(
                proxy_url,
                timeout=15000,
                wait_until="domcontentloaded"
            )

            html = await page.content()

            soup = BeautifulSoup(
                html,
                'html.parser'
            )

            jobs = []

            cards = soup.select(
                ".individual_internship"
            )

            print(f"Found {len(cards)} cards")

            for card in cards:

                try:

                    title_elem = card.select_one(
                        ".job-internship-name"
                    )

                    company_elem = card.select_one(
                        ".company-name"
                    )

                    link_elem = card.select_one(
                        "a[href*='/internship/detail/']"
                    )

                    if not title_elem or not link_elem:
                        continue

                    title = title_elem.get_text(
                        strip=True
                    )

                    company = (
                        company_elem.get_text(strip=True)
                        if company_elem
                        else "Unknown Company"
                    )

                    link = (
                        "https://internshala.com"
                        + link_elem["href"]
                    )

                    # ---------------- LOCATION ----------------

                    location_elem = card.select_one(
                        ".locations"
                    )

                    location = (
                        location_elem.get_text(strip=True)
                        if location_elem
                        else "Remote"
                    )

                    # ---------------- STIPEND ----------------

                    stipend_elem = card.select_one(
                        ".stipend"
                    )

                    stipend = (
                        stipend_elem.get_text(strip=True)
                        if stipend_elem
                        else "Not Disclosed"
                    )

                    # ---------------- DURATION ----------------

                    duration = "N/A"

                    all_text = card.get_text(
                        " ",
                        strip=True
                    )

                    match = re.search(
                        r"\d+\s*(Month|Months)",
                        all_text,
                        re.IGNORECASE
                    )

                    if match:

                        duration = match.group(0)

                    jobs.append({

                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Stipend": stipend,
                        "Duration": duration,
                        "Link": link

                    })

                except Exception as e:

                    print(
                        "Card parse failed:",
                        e
                    )

            return jobs

        finally:

            await browser.close()