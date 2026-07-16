# Hermes — BAC Math Study Hub

A Flask app: math topics, exercises, formula sheets, and practice exams for
Première BAC students. Free for visitors — you just pay a small hosting bill
to keep it running.

## What changed from your original file

- **Per-visitor progress**: progress used to live in one global dictionary
  shared by every single visitor (everyone saw the same numbers, and they
  reset whenever the server restarted). It's now stored per-visitor in a
  signed session cookie via `get_progress()` / `save_progress()`.
- **Production-ready startup**: reads `PORT` and `FLASK_DEBUG` from
  environment variables instead of hardcoding `debug=True, port=8080`.
- Added `requirements.txt`, `Procfile` (gunicorn) for hosting platforms.

## Before you deploy

Set a real `SECRET_KEY` environment variable (don't use the fallback dev key):

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Copy that value into your host's environment variable settings as `SECRET_KEY`.

## Deploying (Render — simplest free/cheap option for a Flask app like this)

1. Push this folder to a GitHub repo.
2. Go to render.com → New → Web Service → connect the repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Add environment variable `SECRET_KEY` (value from above) and
   `FLASK_DEBUG=0`.
6. Deploy. Render gives you a public `https://your-app.onrender.com` URL.

Railway and Fly.io work almost identically — same `requirements.txt` and
`Procfile`, just a different dashboard for connecting the repo and setting
the env vars.

## Running locally (unchanged)

```bash
pip install -r requirements.txt
python3 app.py
```

Visits `http://127.0.0.1:8080` same as before.
