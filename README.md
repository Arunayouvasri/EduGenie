# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project documentation. It provides:

- Q&A
- Beginner-friendly concept explanations
- 3-question MCQ quiz generation
- Text summarization
- Personalized learning paths

## Architecture

```text
Browser
  │
  ├── HTML/CSS/JavaScript
  │
  ▼
FastAPI (`main.py`)
  │
  ├── `/qa` ───────────────► qna.py
  ├── `/explain` ───────────► explanation_module.py
  ├── `/quiz` ──────────────► quiz_module.py
  ├── `/summarize` ─────────► summary_module.py
  └── `/learn/recommendations` ─► learning_path.py
                              │
                              ▼
                     Google Gemini API
```

## Why the Gemini model is updated

The original document names Gemini 1.5 Pro. That model is no longer the appropriate current choice for a new implementation, so this project uses the current Google GenAI SDK and a stable Gemini model through the `GEMINI_MODEL` setting. The default is `gemini-2.5-flash`; you can change it without editing Python code.

## VS Code setup — Windows

### 1. Install Python

Use Python 3.10 or newer. In a new VS Code terminal:

```powershell
python --version
```

### 2. Open the project

In VS Code, open the `EduGenie` folder.

### 3. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If PowerShell blocks activation, you can use:

```powershell
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Gemini

Copy `.env.example` to `.env` and put your Gemini API key in it:

```text
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
USE_LOCAL_EXPLAINER=false
```

Do not commit `.env` to GitHub. It is already excluded by `.gitignore`.

### 6. Start the server

```powershell
uvicorn main:app --reload
```

Open:

`http://127.0.0.1:8000`

## Testing the application

### Browser tests

Try these one by one:

1. **Ask:** `Which is the largest ocean?`
2. **Explain:** `Pythagoras theorem`
3. **Quiz:** paste a short paragraph about the water cycle.
4. **Summarize:** paste your class notes.
5. **Learning Path:** `SQL`, choose Beginner.

### API health test

Open:

`http://127.0.0.1:8000/health`

Expected response:

```json
{"status":"ok","service":"EduGenie"}
```

### Automated test

Install pytest if you want to run the included tests:

```powershell
pip install pytest
pytest
```

## Optional local explanation model

The source document proposes LaMini-Flan-T5-783M for explanations. The implementation keeps that option in `explanation_module.py`, but it is disabled by default so the normal setup remains lightweight.

To enable it:

```powershell
pip install transformers torch
```

Then set:

```text
USE_LOCAL_EXPLAINER=true
```

The first run downloads the model and can require substantial disk space/RAM. All other EduGenie functions continue to use Gemini.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health check |
| POST | `/qa` | Question answering |
| POST | `/explain` | Concept explanation |
| POST | `/quiz` | Three MCQs |
| POST | `/summarize` | Summary |
| POST | `/learn/recommendations` | Learning path |

FastAPI also provides interactive API documentation at:

`http://127.0.0.1:8000/docs`

## Common problems

**`GEMINI_API_KEY is not configured`**

Make sure the file is named exactly `.env`, it is in the project root, and the key is on the `GEMINI_API_KEY=` line. Restart Uvicorn after changing `.env`.

**`ModuleNotFoundError`**

Activate `.venv` and run `pip install -r requirements.txt` again.

**Port 8000 already in use**

Run:

```powershell
uvicorn main:app --reload --port 8001
```

Then open `http://127.0.0.1:8001`.

## Security notes

- The Gemini key stays on the FastAPI server and is not placed in frontend JavaScript.
- `.env` is ignored by Git.
- The API validates request sizes using Pydantic.
- AI output should still be checked by learners before relying on it for high-stakes academic or factual decisions.
