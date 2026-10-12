import os
import html
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalEase - AI Powered Legal Document Generator")


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LegalEase</title>
        <style>
            body {
                font-family: Arial;
                background: #f2f4f7;
                padding: 30px;
            }

            .container {
                max-width: 800px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
            }

            h1 {
                text-align: center;
            }

            label {
                font-weight: bold;
                display: block;
                margin-top: 15px;
            }

            input, textarea, select {
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                box-sizing: border-box;
            }

            textarea {
                height: 100px;
            }

            button {
                margin-top: 20px;
                padding: 12px 25px;
                background: black;
                color: white;
                border: none;
                border-radius: 7px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>

    <div class="container">

        <h1>⚖️ LegalEase</h1>

        <p style="text-align:center;">
        AI-Powered Legal Document Generator
        </p>

        <form action="/generate" method="get">

            <label>Document Type</label>

            <select name="document_type">
                <option>Rental Agreement</option>
                <option>Employment Agreement</option>
                <option>Non-Disclosure Agreement</option>
                <option>Service Agreement</option>
                <option>Leave and License Agreement</option>
            </select>


            <label>First Party Name</label>
            <input name="party_one" required>


            <label>Second Party Name</label>
            <input name="party_two" required>


            <label>Address / Property Details</label>
            <textarea name="address"></textarea>


            <label>Amount / Rent / Salary</label>
            <input name="amount">


            <label>Agreement Duration</label>
            <input name="duration">


            <label>Additional Terms</label>
            <textarea name="extra_terms"></textarea>


            <button type="submit">
                Generate Legal Document
            </button>

        </form>

    </div>

    </body>
    </html>
    """


@app.get("/generate", response_class=HTMLResponse)
def generate_document(
    document_type: str,
    party_one: str,
    party_two: str,
    address: str = "",
    amount: str = "",
    duration: str = "",
    extra_terms: str = ""
):

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        return """
        <h2>Error</h2>
        <p>GEMINI_API_KEY not found in .env file.</p>
        """


    prompt = f"""
Create a professional draft legal document for educational purposes.

Document Type: {document_type}

First Party: {party_one}

Second Party: {party_two}

Address / Property:
{address}

Amount / Rent / Salary:
{amount}

Duration:
{duration}

Additional Terms:
{extra_terms}

Include:

1. Title
2. Parties
3. Purpose of Agreement
4. Payment / Consideration
5. Duration
6. Responsibilities
7. Termination
8. Dispute Resolution
9. Signatures

Use clear and professional legal language.

At the end include:
"AI-generated draft for educational purposes.
Review by a qualified lawyer before real-world use."
"""


    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"
    )


    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }


    try:

        response = requests.post(
    url,
    headers={
        "x-goog-api-key": api_key,
        "Content-Type": "application/json"
    },
    json=data,
    timeout=90
)
        

    except Exception as e:

        return f"""
        <h2>Connection Error</h2>
        <p>{html.escape(str(e))}</p>
        """


    if response.status_code != 200:

        return f"""
        <h2>Gemini API Error</h2>
        <p>Status Code: {response.status_code}</p>
        <pre>{html.escape(response.text)}</pre>
        """


    result = response.json()


    try:

        document = result["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:

        return f"""
        <h2>Unexpected Gemini Response</h2>
        <pre>{html.escape(str(result))}</pre>
        """


    safe_document = html.escape(document)


    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>LegalEase - Generated Document</title>

        <style>

            body {{
                font-family: Arial;
                background: #f2f4f7;
                padding: 30px;
            }}

            .container {{
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
            }}

            .document {{
                white-space: pre-wrap;
                background: #fafafa;
                padding: 25px;
                border: 1px solid #ddd;
                margin-top: 20px;
            }}

            button {{
                padding: 12px 25px;
                background: black;
                color: white;
                border: none;
                border-radius: 7px;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>⚖️ LegalEase</h1>

            <h2>Generated Legal Document</h2>

            <div class="document">
{safe_document}
            </div>

            <br>

            <button onclick="window.print()">
                Print / Save as PDF
            </button>

            <br><br>

            <a href="/">
                ← Create Another Document
            </a>

        </div>

    </body>

    </html>
    """