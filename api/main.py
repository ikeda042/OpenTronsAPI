from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from slack import send_message_func


class Message(BaseModel):
    message: str


app = FastAPI()


@app.post("/send_message")
async def send_message(msg: Message):
    # await send_message_func(msg.message)
    print(msg.message)
    return {"message": msg.message}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
