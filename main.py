import uvicorn
from os import getenv

if __name__ == "__main__":
	port = int(getenv("PORT", 8000))
	uvicorn.run("app.api_v2:app", host="0.0.0.0", port=port, reload=False)