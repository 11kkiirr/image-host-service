from fastapi import FastAPI
import uvicorn

from core.config import config

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

def main():
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)



if __name__ == "__main__":
    main()