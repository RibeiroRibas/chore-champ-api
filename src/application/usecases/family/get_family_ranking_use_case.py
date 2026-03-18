from src.api.v1.responses.users.family_member_ranking_response import (
    FamilyMemberRankingResponse,
)
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.infra.decorators.logger import logging
from src.repositories.user_repository import UserRepository


class GetFamilyRankingUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @logging(show_args=True, show_return=True)
    def execute(self, family_id: int) -> list[FamilyMemberRankingResponse]:
        try:
            return self.__get_ranking(family_id)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(
                code=InternalErrorCodes.GET_FAMILY_RANKING_ERROR.code()
            )

    def __get_ranking(self, family_id: int) -> list[FamilyMemberRankingResponse]:
        entities = self.user_repository.find_ranking_by_family_id(family_id)
        return [FamilyMemberRankingResponse.from_entity(e) for e in entities]
