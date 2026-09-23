# Day 3 — Local Groq Chat Backend

Small FastAPI backend for the Day 3 workshop. It keeps the Groq API key on the server and makes one Groq chat-completion request for each submitted chat turn.

## Requirements

- Python 3.12
- A Groq API key
- A currently available Groq chat model ID supplied by the instructor

## Setup

From the repository root:

~~~bash
cd day3
python -m venv .venv
~~~

Activate the virtual environment.

Windows PowerShell:

~~~powershell
.\.venv\Scripts\Activate.ps1
~~~

macOS/Linux:

~~~bash
source .venv/bin/activate
~~~

Install dependencies:

~~~bash
python -m pip install -r requirements.txt
~~~

Create your local configuration from the example.

Windows PowerShell:

~~~powershell
Copy-Item .env.example .env
~~~

macOS/Linux:

~~~bash
cp .env.example .env
~~~

Edit day3/.env and replace both placeholders:

~~~text
GROQ_API_KEY=...
GROQ_MODEL=...
~~~

The real .env file is ignored by Git. Environment variables take precedence over values in day3/.env.

## Run

From inside day3/:

~~~bash
python -m uvicorn app:app --reload
~~~

Open the health endpoint:

~~~text
http://127.0.0.1:8000/api/health
~~~

A configured server reports configured: true. The endpoint never calls Groq and never returns the API key.

## Chat request

POST http://127.0.0.1:8000/api/chat

Example body:

~~~json
{
  "messages": [
    {"role": "user", "content": "Hello"}
  ]
}
~~~

Successful response:

~~~json
{
  "reply": "Hello! How can I help?",
  "model": "your-configured-model-id"
}
~~~

Only user and assistant conversation messages are accepted. The server adds its own system instruction, limits message size and conversation length, bounds output, disables SDK retries, and uses an explicit request timeout.

## Notes

- Do not put a real API key in .env.example or source code.
- Restart Uvicorn after changing .env.
- This folder contains only the backend; it does not modify the existing GitHub Pages site.
