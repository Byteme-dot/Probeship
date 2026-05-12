from flask import Flask, request, jsonify
from flask_cors import CORS

import asyncio

from scraper.bot import get_internships
from scraper.bot_pro import get_internships_pro
from scraper.enrich_bot import enrich_single_internship


app = Flask(__name__)

CORS(app)


# ----------------------------------------
# HOME ROUTE
# ----------------------------------------

@app.route("/")
def home():

    return {
        "message": "Flask Backend Running"
    }


# ----------------------------------------
# SEARCH INTERNSHIPS
# ----------------------------------------

@app.route("/search")
def search():

    keyword = request.args.get("keyword")

    mode = request.args.get("mode")

    if not keyword:

        return jsonify([])

    # ---------------- CLEAN KEYWORD ----------------

    keyword = (
        keyword
        .strip()
        .replace(" ", "-")
        .lower()
    )

    print(f"\nSearching for: {keyword}")
    print(f"Mode: {mode}")

    try:

        # ---------------- DEEP SEARCH ----------------

        if mode == "pro":

            results = asyncio.run(
                get_internships_pro(keyword)
            )

        # ---------------- QUICK SEARCH ----------------

        else:

            results = asyncio.run(
                get_internships(keyword)
            )

        print(
            f"Results found: {len(results)}"
        )

        if results:

            print(results[:2])

        print("Returning JSON...")

        return jsonify(results)

    except Exception as e:

        print("\nSEARCH ERROR:")
        print(e)

        return jsonify({

            "error": str(e)

        }), 500


# ----------------------------------------
# ENRICH SINGLE INTERNSHIP
# ----------------------------------------

@app.route(
    "/enrich-single",
    methods=["POST"]
)
def enrich_single():

    try:

        data = request.json

        link = data.get("link")

        if not link:

            return jsonify({

                "error": "No link provided"

            }), 400

        print("\nEnriching internship:")
        print(link)

        result = asyncio.run(
            enrich_single_internship(link)
        )

        print("Enrichment Complete")

        return jsonify(result)

    except Exception as e:

        print("\nENRICH ERROR:")
        print(e)

        return jsonify({

            "error": str(e)

        }), 500


# ----------------------------------------
# START SERVER
# ----------------------------------------

if __name__ == "__main__":

    app.run(

        debug=True,

        use_reloader=False,

        threaded=True
    )