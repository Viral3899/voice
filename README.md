# Healthcare Voice AI Appointment Agent

A local full-stack voice assistant for healthcare reception.

This project includes:

- Speech recognition for user voice input
- Natural language intent understanding with Groq tool calling
- Appointment booking, retrieval, cancellation, and modification
- Voice response synthesis
- Talking avatar and conversation summary support

## Requirements

- Python 3.11+ (recommended)
- Node.js 18+ / npm
- Git (optional)

## Setup

1. Open a terminal in the repository root.
2. Activate the Python virtual environment.

### Bash

```bash
cd /c/Users/viral/Downloads/lll
source venv/Scripts/activate
```

### PowerShell

```powershell
cd C:\Users\viral\Downloads\lll
.\venv\Scripts\Activate.ps1
```

### CMD

```cmd
cd C:\Users\viral\Downloads\lll
venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
make install
```

## Running the app

### Option 1: Start backend and frontend separately

Terminal 1:

```bash
make backend
```

Terminal 2:

```bash
make frontend
```

### Option 2: Start both servers in one command

```bash
python run.py
```

## Application URLs

- Frontend: `http://localhost:5173`
- Backend API: `http://127.0.0.1:8000`

## Files and folders

- `backend/` — FastAPI application, database models, routes, and voice tooling
- `frontend/` — React + Vite user interface
- `run.py` — one-command startup script for backend and frontend
- `Makefile` — project helpers for install, run, and cleanup
- `.gitignore` — repository ignore rules
- `requirement.txt` — Python dependency list

## Environment variables

The backend reads credentials from `.env` if present.

Typical `.env` values:

```text
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...
GROQ_API_KEY=...
GROQ_MODEL=llama-3.1-8b-instant
DATABASE_URL=sqlite:///./voice_ai.db
```

## Notes

- `frontend/.gitignore` excludes `node_modules`, build output, and local environment files.
- The frontend proxies API requests to the backend via `/api`.
- If you see proxy errors, verify the backend is running on port `8000`.
- Generated audio files are stored as `generated_audio.wav`.

## Troubleshooting

- If `make` is unavailable on Windows, run the commands directly.
- If backend imports fail, ensure you are in the repo root and using the activated virtual environment.
- If voice synthesis fails, verify dependencies are installed and the local TTS engine or API key is configured.
