from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
import requests


class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):

    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotification

    def _run(self, message: str) -> str:
        # If message is a dict, extract the correct field
        if isinstance(message, dict):
            if 'description' in message:
                message = message['description']
            elif 'message' in message:
                message = message['message']
            else:
                # Fallback: all to string
                message = str(message)
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: {message}")
        payload = {"user": pushover_user, 
                   "token": pushover_token, 
                   "message": message}
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'