# StyleAI — Complete Recommendation Flow

## What is fixed

The application now has a complete working path:

**Upload photo → choose occasion → choose outfit type → choose color → Get AI Recommendation → recommendation result + next step**

The frontend calls `POST /api/recommend`, the Flask backend saves the image, runs `ai/recommendation.py`, and returns structured recommendation data. If the backend is temporarily unavailable, the frontend shows a local fallback recommendation instead of getting stuck.

## Important limitation

The included recommendation engine is **rule-based**, not a trained computer-vision model. It uses the selected options and confirms the uploaded image was received. It does not infer body shape, skin tone, existing clothing, etc. To add real image understanding, integrate a vision model/API inside `ai/recommendation.py`.

## Windows — easiest way

Double-click:

`run.bat`

The script creates a virtual environment, installs dependencies, starts Flask and opens the browser.

## Manual Windows setup

From the project root:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
python backend\app.py
```

Open:

`http://127.0.0.1:5000`

## macOS/Linux

```bash
chmod +x run.sh
./run.sh
```

Then open `http://127.0.0.1:5000`.

## Folder map

- `frontend/index.html` — page and recommendation result section
- `frontend/style.css` — styling
- `frontend/script.js` — upload, validation, API call, loading state, result rendering and fallback
- `backend/app.py` — Flask server and `/api/recommend` endpoint
- `backend/requirements.txt` — Python packages
- `ai/recommendation.py` — recommendation engine
- `uploads/` — uploaded photos
- `database/database.sql` — optional MySQL schema
- `run.bat` — one-click Windows startup
- `run.sh` — macOS/Linux startup

## If the button still appears not to work

Do not double-click the HTML as your normal workflow. Start the server with `run.bat` or `python backend/app.py`, then open `http://127.0.0.1:5000`. The browser should show the recommendation section automatically after clicking **Get AI Recommendation**.
