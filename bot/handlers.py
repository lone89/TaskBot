from pyrogram.types import Message
from pyrogram import Client
from sqlalchemy.ext.asyncio import AsyncSession

from factory import task_inline_factory
from constants import (
    MANAGE_TASK_INLINE_KEYBOAR_MARKUP,
    NO_TASKS_INLINE_KEYBOAR_MARKUP,
    TASKS_INLINE_KEYBOAR_MARKUP,
)
from db import (
    create_task,
    delete_task,
    get_task__by_title,
    get_tasks,
    update_task_status,
)


async def handle_create_task(
    client: Client,
    message: Message,
    user_id: int,
    session_factory: AsyncSession,
    **kwargs,
) -> None:
    """
    Handles the creation of a task.
    """

    title = await client.ask(message.chat.id, "Введите название задачи: ")
    description = await client.ask(message.chat.id, "Введите описание задачи: ")

    await create_task(
        telegram_id=user_id,
        title=title.text,
        description=description.text,
        session_factory=session_factory,
    )

    await message.reply(
        "Задача успешно создана!", reply_markup=TASKS_INLINE_KEYBOAR_MARKUP
    )


async def handle_view_tasks(
    message: Message,
    user_id: int,
    is_done: bool,
    session_factory: AsyncSession,
    **kwargs,
) -> None:
    """
    Handles viewing tasks.
    """

    tasks = await get_tasks(
        telegram_id=user_id,
        session_factory=session_factory,
        is_done=is_done,
    )

    if tasks:
        await message.reply(
            "Список задач!", reply_markup=task_inline_factory(tasks=tasks)
        )
    else:
        await message.reply(
            "У вас нет задач!", reply_markup=NO_TASKS_INLINE_KEYBOAR_MARKUP
        )


async def handle_update_task_status(
    message: Message, user_id: int, session_factory: AsyncSession, **kwargs
) -> None:
    """
    Handles updating task status.
    """

    await update_task_status(
        session_factory=session_factory, telegram_id=user_id, title=message.text
    )

    await message.reply(
        "Задача успешно обновлена!", reply_markup=TASKS_INLINE_KEYBOAR_MARKUP
    )


async def handle_delete_task(
    message: Message, user_id: int, session_factory: AsyncSession, **kwargs
) -> None:
    """
    Handles deleting a task.
    """

    await delete_task(
        telegram_id=user_id,
        task_title=message.text,
        session_factory=session_factory,
    )

    await message.reply(
        "Задача успешно удалена!", reply_markup=TASKS_INLINE_KEYBOAR_MARKUP
    )


async def handle_task_description(
    message: Message, user_id: int, session_factory: AsyncSession, **kwargs
) -> None:
    """
    Handles displaying the description of a task.
    """

    task = await get_task__by_title(
        telegram_id=user_id,
        task_title=message.text,
        session_factory=session_factory,
    )

    await message.reply(f"{task.description}", reply_markup=TASKS_INLINE_KEYBOAR_MARKUP)


async def handle_default(message: Message, data, **kwargs) -> None:
    """
    Handles default behavior related to task's name.
    """

    await message.reply(f"{data}", reply_markup=MANAGE_TASK_INLINE_KEYBOAR_MARKUP)
