import os
import asyncio
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.socket_mode.aiohttp import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse

# DINE TOKENS HER
SLACK_BOT_TOKEN = "xoxb-6073364579488-8805817891893-1FOLA0Aor6u0i3viBXr7zPhS"
SLACK_APP_TOKEN = "xapp-1-A08PAQW05FZ-8813190046514-eebf42f4d0d4879673d9f522617c4c3dd2e19615ffa62e437d6e45d07e0d8edc"
OPENAI_API_KEY = "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"


class SlackBot:

    def __init__(self):
        self.client = AsyncWebClient(token=SLACK_BOT_TOKEN)
        self.socket_mode_client = None

    async def process(self, client, req: SocketModeRequest):
        if req.type == "events_api":
            event = req.payload["event"]
            print(
                f"🔵 Event modtaget: {event}")  # <--- Viser event i terminalen

            if event.get("type") == "app_mention":
                channel = event["channel"]
                user_text = event.get("text", "")
                await client.web_client.chat_postMessage(
                    channel=channel, text=f"👋 Hej! Jeg modtog: {user_text}")
            elif event.get("type") == "message" and "text" in event:
                text = event["text"].lower()
                if text.startswith("/opdater"):
                    await client.web_client.chat_postMessage(
                        channel=event["channel"],
                        text="🔄 Opdatering påbegyndt... (Simuleret auto-update)"
                    )
            await client.send_socket_mode_response(
                SocketModeResponse(envelope_id=req.envelope_id))

    async def start(self):
        self.socket_mode_client = SocketModeClient(app_token=SLACK_APP_TOKEN,
                                                   web_client=self.client)
        self.socket_mode_client.socket_mode_request_listeners.append(
            self.process)
        await self.socket_mode_client.connect()
        print("🚀 MM Bot er klar og lytter på beskeder...")
        await asyncio.Event().wait()


if __name__ == "__main__":
    bot = SlackBot()
    asyncio.run(bot.start())
