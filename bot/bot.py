import asyncio
import os

from pyromod import Client
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from handlers import setup_handlers
from models import init_db


class Bot:
    def __init__(self) -> None:
        self.api_id = os.getenv("API_ID")
        self.api_hash = os.getenv("API_HASH")
        self.bot_token = os.getenv("BOT_TOKEN")
        self.bot_name = os.getenv("BOT_NAME")
        self.db_url = os.getenv("DATABASE_URL")

        self.client = Client(
            self.bot_name,
            api_id=self.api_id,
            api_hash=self.api_hash,
            bot_token=self.bot_token,
        )

        self.engine = create_async_engine(self.db_url, echo=True, future=True)
        self.session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def initialize(self) -> None:
        """
        Initializes the bot.

        Sets up the database and registers command handlers.
        """
        await init_db(self.engine)
        await setup_handlers(self.client, self.session)

    def run(self) -> None:
        """
        Runs the bot.

        Creates an event loop, initializes the bot, and starts the Pyrogram client.
        """
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.initialize())
        self.client.run()


if __name__ == "__main__":
    bot = Bot()
    bot.run()
