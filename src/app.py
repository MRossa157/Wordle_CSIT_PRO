from fastapi import FastAPI

app = FastAPI(title='Worlde backend')


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}
