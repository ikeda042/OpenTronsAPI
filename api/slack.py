import os
import json
import aiohttp


async def send_message_func(text: str):
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    print(webhook_url)
    message = {"text": text}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            webhook_url,
            data=json.dumps(message),
            headers={"Content-Type": "application/json"},
        ) as response:
            if response.status == 200:
                print("Message sent successfully")
            else:
                print(
                    f"Failed to send message: {response.status}, {await response.text()}"
                )
