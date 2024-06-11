from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

REGISTER_KEYBOARD_MARKUP = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton("/register"),
        ],
    ],
    resize_keyboard=True,
)


REPLY_KEYBOARD_MARKUP = ReplyKeyboardMarkup(
    [
        [KeyboardButton("/create_task")],
        [
            KeyboardButton("/completed_tasks"),
            KeyboardButton("/non_completed_tasks"),
        ],
    ],
    resize_keyboard=True,
)


TASKS_INLINE_KEYBOAR_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Создать задачу", callback_data="create_task"),
        ],
        [
            InlineKeyboardButton(
                "Просмотреть выполненные задачи", callback_data="completed_tasks"
            ),
            InlineKeyboardButton(
                "Просмотреть невыполненные задачи", callback_data="non_completed_tasks"
            ),
        ],
    ]
)


NO_TASKS_INLINE_KEYBOAR_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Создать задачу", callback_data="create_task"),
        ],
    ]
)


MANAGE_TASK_INLINE_KEYBOAR_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Описание", callback_data="task_description"),
        ],
        [
            InlineKeyboardButton("Выполнена", callback_data="update_task_status"),
            InlineKeyboardButton("Удалить задачу", callback_data="delete_task"),
        ],
    ]
)
