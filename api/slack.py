import requests
import json
import os


webhook_url = os.environ["SLACK_WEBHOOK_URL"]

message = {"text": "payload test"}

response = requests.post(
    webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    print("Message sent successfully")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
