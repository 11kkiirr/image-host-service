from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from core.config import config
from presentation.api.routes import router as api_router


app = FastAPI()
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем запросы откуда угодно для тестов
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

def main():
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)



if __name__ == "__main__":
    main()