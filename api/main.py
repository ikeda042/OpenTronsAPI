from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/{message}")
async def send_message(message: str):
    return {"message": message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
