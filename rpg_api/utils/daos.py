from rpg_api.web.daos.base_user_dao import BaseUserDAO
from rpg_api.web.daos.base_character_dao import BaseCharacterDAO
from rpg_api.web.daos.base_class_dao import BaseClassDAO


from rpg_api.db.postgres.dependencies import get_db_session
from rpg_api.db.postgres.session import AsyncSessionWrapper as AsyncSession
from fastapi import Depends
from typing import Annotated


class AllDAOs:
    """Class for accessing all DAOs."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session

    @property
    def base_user(self) -> BaseUserDAO:
        """Base user DAO."""
        return BaseUserDAO(session=self.session)

    @property
    def base_character(self) -> BaseCharacterDAO:
        """Base character DAO."""
        return BaseCharacterDAO(session=self.session)

    @property
    def base_class(self) -> BaseClassDAO:
        """Base class DAO."""
        return BaseClassDAO(session=self.session)


GetDAOs = Annotated[AllDAOs, Depends(AllDAOs)]
