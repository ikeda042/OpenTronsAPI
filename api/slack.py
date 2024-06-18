import requests
import json
import os

# Webhook URL
webhook_url = os.environ["SLACK_WEBHOOK_URL"]
# 送信するメッセージのペイロード
message = {"text": "Hello, this is a test message from Python!"}

# POSTリクエストを送信
response = requests.post(
    webhook_url, data=json.dumps(message), headers={"Content-Type": "application/json"}
)

# レスポンスを確認
if response.status_code == 200:
    print("Message sent successfully")
else:
    print(f"Failed to send message: {response.status_code}, {response.text}")
