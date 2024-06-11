from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import Task, User


async def get_user__by_id(user_id: int, session_factory: AsyncSession) -> User | None:
    """
    Retrieves a user by their ID.

    """
    async with session_factory() as session:
        result = await session.execute(select(User).where(User.telegram_id == user_id))
        return result.scalar_one_or_none()


async def get_user__by_login(login: str, session_factory: AsyncSession) -> User | None:
    """
    Retrieves a user by their login.

    """
    async with session_factory() as session:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()


async def create_user(
    user_id: int, username: str, login: str, session_factory: AsyncSession
) -> None:
    """
    Creates a new user.

    Adds a user with the specified data to the database.
    """

    async with session_factory() as session:
        user = User(telegram_id=user_id, username=username, login=login)
        session.add(user)

        await session.commit()


async def create_task(
    telegram_id: int, title: str, description: str, session_factory: AsyncSession
) -> Task:
    """
    Creates a new task for a user.

    Adds a new task with the specified title and description to the database for a user with the specified ID.
    """

    async with session_factory() as session:
        user = await get_user__by_id(
            user_id=telegram_id, session_factory=session_factory
        )

        new_task = Task(title=title, description=description, user=user)
        session.add(new_task)

        await session.commit()
        await session.refresh(new_task)

        return new_task


async def get_tasks(
    telegram_id: int, session_factory: AsyncSession, is_done: bool = False
) -> list[Task]:
    """
    Retrieves a list of user tasks.

    Returns a list of user tasks with the specified ID, depending on the is_done flag.
    """

    async with session_factory() as session:
        user = await get_user__by_id(
            user_id=telegram_id, session_factory=session_factory
        )

        tasks_query = await session.execute(
            select(Task).filter((Task.user_id == user.id) & (Task.is_done == is_done))
        )
        tasks = tasks_query.scalars().all()

        return tasks


async def get_task__by_title(
    telegram_id: int, task_title: str, session_factory: AsyncSession
) -> list[Task]:
    """
    Retrieves a user task by its title.

    Returns a task with the specified title for a user with the specified ID.
    """

    async with session_factory() as session:
        user = await get_user__by_id(
            user_id=telegram_id, session_factory=session_factory
        )

        tasks_query = await session.execute(
            select(Task).filter((Task.user_id == user.id) & (Task.title == task_title))
        )
        tasks = tasks_query.scalar_one_or_none()

        return tasks


async def delete_task(
    telegram_id: int, task_title: str, session_factory: AsyncSession
) -> None:
    """
    Deletes a user task.

    Deletes a task with the specified title for a user with the specified ID.
    """

    async with session_factory() as session:
        try:
            user = await get_user__by_id(
                user_id=telegram_id, session_factory=session_factory
            )
            task_query = await session.execute(
                select(Task).where((Task.title == task_title) & (Task.user == user))
            )
            task = task_query.scalar_one_or_none()

            await session.delete(task)
            await session.commit()

        except Exception as e:
            await session.rollback()
            raise e


async def update_task_status(
    session_factory: AsyncSession, telegram_id: int, title: str = None
) -> Task:
    """
    Updates the status of a task.

    Marks a task with the specified title as done for a user with the specified ID.
    """

    async with session_factory() as session:
        try:
            user = await get_user__by_id(
                user_id=telegram_id, session_factory=session_factory
            )

            task_query = await session.execute(
                select(Task).where(Task.title == title, Task.user == user)
            )
            task = task_query.scalars().one()

            task.is_done = True

            await session.commit()
            await session.refresh(task)
            return task

        except NoResultFound:
            raise ValueError("Task not found")
        except Exception as e:
            await session.rollback()
            raise e
