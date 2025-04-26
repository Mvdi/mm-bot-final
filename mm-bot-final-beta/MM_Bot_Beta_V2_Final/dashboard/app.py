from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
import os
import time

# INDSÆTTE DINE EGNE TOKENS HER
SLACK_APP_TOKEN = "xapp-1-A08PAQW05FZ-8813190046514-eebf42f4d0d4879673d9f522617c4c3dd2e19615ffa62e437d6e45d07e0d8edc"
SLACK_BOT_TOKEN = "-8805817891893-1FOLA0Aor6u0i3viBXr7zPhS"

# OPRET SLACK CLIENTS
web_client = WebClient(token=SLACK_BOT_TOKEN)
socket_client = SocketModeClient(
    app_token=SLACK_APP_TOKEN,
    web_client=web_client
)

# DEFINER EVENT HANDLER
def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        event = req.payload["event"]
        if event.get("type") == "app_mention":  # Når botten nævnes
            channel = event["channel"]
            user_text = event.get("text", "")
            web_client.chat_postMessage(
                channel=channel,
                text=f"👋 Hej! Jeg modtog: {user_text}"
            )
        client.ack(req)

# TILFØJ EVENT HANDLER
socket_client.socket_mode_request_listeners.append(process)

# START SOCKET MODE CLIENT
if __name__ == "__main__":
    socket_client.connect()
    while True:
        time.sleep(1)