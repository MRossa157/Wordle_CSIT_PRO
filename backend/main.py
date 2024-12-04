import uvicorn

from backend.app import app
from backend.config import settings

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.BACK_HOST,
        port=settings.BACK_PORT,
    )
