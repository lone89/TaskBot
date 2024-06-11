from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models import Task


def task_inline_factory(tasks: list[Task]) -> InlineKeyboardMarkup:
    """
    Factory function that generates a task matrix for correct display in the inline menu.
    """
    result = []
    tasks_list = []

    for index, task in enumerate(tasks):
        tasks_list.append(
            InlineKeyboardButton(f"{task.title}", callback_data=f"{task.title}")
        )
        if (index + 1) % 3 == 0:
            result.append(tasks_list)
            tasks_list = []

    if tasks_list:
        result.append(tasks_list)

    return InlineKeyboardMarkup(result)
