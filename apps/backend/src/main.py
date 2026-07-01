from fastapi import FastAPI
import uvicorn

from core.config import config
from presentation.api.routes.auth_route import router as auth_router
from presentation.api.routes.profile_route import router as profile_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(profile_router)

def main():
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)



if __name__ == "__main__":
    main()