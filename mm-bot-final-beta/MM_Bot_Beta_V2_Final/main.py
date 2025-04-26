import asyncio
from utils.slack_bot import SlackBot


async def main():
    bot = SlackBot()
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
