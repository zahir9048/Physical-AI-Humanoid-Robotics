"""
Hugging Face Spaces entry point for FastAPI backend.
This file is required by Hugging Face Spaces to run the application.
"""
import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.api.main import app

# Hugging Face Spaces will automatically run this on port 7860
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
