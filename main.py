import uvicorn

from app import app
from core.config import settings

if __name__ == '__main__':
    # noinspection PyTypeChecker
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
