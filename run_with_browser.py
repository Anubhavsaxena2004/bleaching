import webbrowser
import time
import subprocess
import sys
import os

if __name__ == "__main__":
    # Start FastAPI backend
    backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload"])
    # Start HTTP server for frontend (on port 8080)
    # Use Python 3's http.server module
    frontend = subprocess.Popen([sys.executable, "-m", "http.server", "8080"], cwd=os.path.dirname(os.path.abspath(__file__)))
    # Wait a bit for both servers to start
    time.sleep(2)
    # Open the frontend in the browser
    webbrowser.open_new_tab("http://localhost:8080/index.html")
    try:
        # Wait for backend to finish (Ctrl+C to stop)
        backend.wait()
    finally:
        frontend.terminate()
