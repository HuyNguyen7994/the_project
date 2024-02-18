import uvicorn
from backend.main import app


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)