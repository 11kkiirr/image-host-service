from types import TracebackType
from typing import Callable, Optional, Type, TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from core.db.engine import session_maker


from database.repositories.users import UserRepository
from database.repositories.files import FileRepository
from database.repositories.items import ItemRepository


class UnitOfWork:
    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self):
        self._session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):  # exc_type, exc_val, exc_tb
        if self._session:
            if exc_type:
                await self._session.rollback()
            else:
                await self._session.commit()
            await self._session.close()
            self._session = None

    @property
    def _active_session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError(
                "Сессия UoW не активна. Используйте UnitOfWork в контекстном менеджере 'async with'."
            )
        return self._session

    @property
    def session(self) -> AsyncSession:
        return self._active_session

    @property
    def users(self) -> "UserRepository":
        return UserRepository(self._active_session)
    
    @property
    def files(self) -> "FileRepository":
        return FileRepository(self._active_session)
    @property
    def items(self) -> "ItemRepository":
        return ItemRepository(self._active_session)


def get_uow() -> UnitOfWork:
    return UnitOfWork(session_factory=session_maker)