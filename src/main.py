from os import getenv

import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        app='src.app:app',
        host=getenv('BACK_HOST'),
        port=int(getenv('BACK_PORT')),
    )
