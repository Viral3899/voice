# Root Makefile for the Healthcare Voice AI project

.PHONY: help backend frontend install clean env

help:
	@echo "Available targets:"
	@echo "  install   - install Python and frontend dependencies"
	@echo "  backend   - start the FastAPI backend server"
	@echo "  frontend  - start the Vite React frontend"
	@echo "  env       - show how to activate the Python virtual environment"
	@echo "  clean     - remove generated audio and temporary files"

install:
	@echo "Installing Python dependencies..."
	pip install -r requirement.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

backend:
	@echo "Starting backend on http://127.0.0.1:8000"
	python backend/main.py

frontend:
	@echo "Starting frontend on http://localhost:5173"
	cd frontend && npm run dev

env:
	@echo "Activate the Python virtual environment with one of these commands:"
	@echo "  Bash: source venv/Scripts/activate"
	@echo "  PowerShell: .\\venv\\Scripts\\Activate.ps1"
	@echo "  CMD: venv\\Scripts\\activate.bat"

clean:
	@echo "Cleaning generated files..."
	rm -f generated_audio.wav
