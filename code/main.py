import fastapi
import uvicorn

from typing import Optional

api = fastapi.FastAPI()


@api.get('/hello')
def greeting():
    return 'Hello, World!'

@api.get('/hola')
def greeting_es():
    return 'Hola, Test!'


if __name__ ==  '__main__':
    uvicorn.run(api)