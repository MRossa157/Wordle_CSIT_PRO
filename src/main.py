import uvicorn

from src.config import settings

if __name__ == '__main__':
    uvicorn.run(
        app='src.app:app',
        host=settings.BACK_HOST,
        port=settings.BACK_PORT,
    )
