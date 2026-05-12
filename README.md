# PROBESHIP

Modern Internship Discovery Platform

PROBESHIP is a full-stack internship scraping and enrichment platform built using Flask, Playwright, and JavaScript.

The platform automates internship discovery using browser automation, deep-search extraction, and asynchronous enrichment systems while presenting results in a modern responsive UI.

---

# Features

* Quick Search Mode
* Deep Search Mode using ScraperAPI
* Automatic Skills Enrichment
* Progressive Loading
* Dark / Light Theme
* Location & Paid Filters
* Responsive Internship Cards
* Async Enrichment Architecture

---

# Tech Stack

## Backend

* Python
* Flask
* Playwright
* BeautifulSoup4
* aiohttp
* AsyncIO

## Frontend

* HTML
* CSS
* JavaScript

## APIs & Tools

* ScraperAPI
* python-dotenv

---

# Setup & Installation

## Clone Repository

```bash
git clone <your_repo_url>
```

## Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

## Create Environment File

Create a `.env` file in the project root:

```env
SCRAPER_API_KEY=your_api_key_here
```

Deep Search mode requires a ScraperAPI key.
Enrichment feature also requires ScraperAPI key.

## Get your own ScraperAPI Key

Go to:
https://dashboard.scraperapi.com/login

Create or login to your account, copy your API key from the dashboard, and paste it into the `.env` file.

---

# Running the Project

## Recommended Method

Run:

```text
auto_start.bat
```

This automatically starts:

* backend server
* frontend server

---

## Manual Method

### Backend

```bash
cd backend
python main.py
```

### Frontend

```bash
cd frontend
python -m http.server 5500
```

---

# Access the Website

Frontend:

```text
http://localhost:5500
```

Backend:

```text
http://127.0.0.1:5000
```

---

# Architecture Overview

1. User searches internships from frontend.
2. Flask backend receives requests.
3. Playwright scrapes internship listings.
4. Deep Search routes requests through ScraperAPI.
5. BeautifulSoup extracts internship details.
6. Frontend dynamically renders cards.
7. Visible internships are enriched asynchronously.
8. Additional results load progressively using Load More.

---

# Key Functionalities

## Skills Enrichment

Visible internship cards are dynamically enriched with required skills.

## Progressive Loading

Internships load incrementally instead of rendering all results simultaneously.

## Frontend Filtering

Users can filter internships based on:

* location
* paid/unpaid internships

without additional backend requests.

---

# Learning Outcomes

This project provided practical experience in:

* browser automation
* async Python programming
* frontend/backend integration
* REST API architecture
* web scraping systems
* dynamic frontend rendering
* anti-bot protection handling
* UI/UX design

---

# Future Improvements

* AI-powered recommendations
* Resume matching
* Bookmark system
* Advanced sorting
* Multi-platform aggregation
* Cloud deployment

---

# Author

Abhishek Kumar

---

# License

Educational / Learning Project
