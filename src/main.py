import uvicorn

from src.app import app
from src.config import settings

if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host=settings.BACK_HOST,
        port=settings.BACK_PORT,
    )
