import uvicorn

from src.config import AppSettings

if __name__ == '__main__':
    app_settings = AppSettings()
    uvicorn.run(
        app='src.app:app',
        host=app_settings.BACK_HOST,
        port=app_settings.BACK_PORT,
    )
