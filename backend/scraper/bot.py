import asyncio
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

USER_AGENT_MAP = {

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36": "Chrome",

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0": "Firefox"
}


async def get_internships(search_query):

    async with async_playwright() as p:

        browser = await p.firefox.launch(
            headless=True
        )

        try:

            random_ua = random.choice(
                list(USER_AGENT_MAP.keys())
            )

            context = await browser.new_context(
                user_agent=random_ua,
                viewport={
                    'width': 1920,
                    'height': 1080
                }
            )

            page = await context.new_page()

            await page.add_init_script(
                """
                Object.defineProperty(
                    navigator,
                    'webdriver',
                    {get: () => undefined}
                )
                """
            )

            url = (
                f"https://internshala.com/"
                f"internships/keywords-{search_query}"
            )

            print(f"Searching: {search_query}")

            await asyncio.sleep(
                random.uniform(1, 3)
            )

            await page.goto(
                url,
                wait_until="domcontentloaded"
            )

            try:

                await page.wait_for_selector(
                    ".individual_internship",
                    timeout=10000
                )

            except:

                print("No internships found.")

                return []

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