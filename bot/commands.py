from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from db import create_user, get_user__by_id, get_user__by_login
from constants import (
    REGISTER_KEYBOARD_MARKUP,
    REPLY_KEYBOARD_MARKUP,
    TASKS_INLINE_KEYBOAR_MARKUP,
)
from handlers import (
    handle_create_task,
    handle_default,
    handle_delete_task,
    handle_task_description,
    handle_update_task_status,
    handle_view_tasks,
)


async def setup_handlers(client: Client, session_factory: AsyncSession) -> None:
    """
    Sets up message and callback handlers for the bot.
    """

    @client.on_message(filters.command("start"))
    async def start(client: Client, message: Message) -> None:
        """
        Handles the '/start' command.

        Sends a welcome message to the user and prompts them to register.
        """
        user = await get_user__by_id(
            user_id=message.from_user.id, session_factory=session_factory
        )

        if user:
            await message.reply(
                f"Здравствуйте, {user.username}! Вы уже зарегистрированы.",
                reply_markup=REPLY_KEYBOARD_MARKUP,
            )

            await message.reply(
                f"Выберите одну из команд:",
                reply_markup=TASKS_INLINE_KEYBOAR_MARKUP,
            )
        else:
            await message.reply(
                "Здравствуйте! Зарегистрируйтесь с помощью меню.",
                reply_markup=REGISTER_KEYBOARD_MARKUP,
            )

    @client.on_message(filters.command("register"))
    async def register(client: Client, message: Message) -> None:
        """
        Handles the '/register' command.

        Prompts the user to enter their name and a unique login. Registers the user if the login is available.
        """

        username = await client.ask(message.chat.id, "Введите ваше имя:")
        login = await client.ask(
            message.chat.id, "Отлично! Сейчас введите уникальный логин:"
        )

        if username and login:
            username, login = username.text, login.text

        user = await get_user__by_login(login=login, session_factory=session_factory)

        if user:
            await message.reply("Этот логин уже используется. Используйте другой:")
            return

        await create_user(
            username=username,
            login=login,
            user_id=message.from_user.id,
            session_factory=session_factory,
        )

        await message.reply(
            f"Спасибо за регистрацию, {username}!", reply_markup=REPLY_KEYBOARD_MARKUP
        )

        await message.reply(
            "Выберите одну из опций ниже:", reply_markup=TASKS_INLINE_KEYBOAR_MARKUP
        )

    @client.on_message(filters.command("create_task"))
    async def create_task(client: Client, message: Message) -> None:
        """
        Handles the '/create_task' command.

        Prompts the user to create a new task.
        """
        user = await get_user__by_id(
            user_id=message.from_user.id, session_factory=session_factory
        )

        await handle_create_task(
            client=client,
            message=message,
            user_id=user.telegram_id,
            session_factory=session_factory,
        )

    @client.on_message(filters.command(["completed_tasks", "non_completed_tasks"]))
    async def non_completed_tasks(client: Client, message: Message) -> None:
        """
        Handles the '/completed_tasks' and '/non_completed_tasks' commands.

        Displays either completed or non-completed tasks based on the command.
        """
        user = await get_user__by_id(
            user_id=message.from_user.id, session_factory=session_factory
        )

        command = message.command[0]
        is_done = command == "completed_tasks"

        await handle_view_tasks(
            message=message,
            user_id=user.telegram_id,
            is_done=is_done,
            session_factory=session_factory,
        )

    @client.on_message(filters.text)
    async def non_completed_tasks(client: Client, message: Message) -> None:
        """
        Handles messages with unknown commands.

        Replies to the user indicating that the command is not recognized.
        """
        await message.reply(
            "Я не знаю такой команды, используйте одну из доступных:",
            reply_markup=TASKS_INLINE_KEYBOAR_MARKUP,
        )

    @client.on_callback_query()
    async def callback_task_handler(client, callback_query: CallbackQuery) -> None:
        """
        Handles callback queries from inline keyboards.

        Routes the callback query to the appropriate handler based on the data.
        """

        tasks_mapping = {
            "create_task": handle_create_task,
            "completed_tasks": handle_view_tasks,
            "non_completed_tasks": handle_view_tasks,
            "update_task_status": handle_update_task_status,
            "delete_task": handle_delete_task,
            "task_description": handle_task_description,
        }

        task_handler = tasks_mapping.get(callback_query.data, handle_default)
        is_done = callback_query.data == "completed_tasks"

        return await task_handler(
            client=client,
            message=callback_query.message,
            user_id=callback_query.from_user.id,
            session_factory=session_factory,
            data=callback_query.data,
            is_done=is_done,
        )
