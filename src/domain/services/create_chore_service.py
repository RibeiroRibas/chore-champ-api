from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.create_chore_dto import CreateChoreDTO
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.dto.users.add_user_points_dto import AddUserPointsDTO
from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.services.detect_new_reward_unlocked_service import (
    DetectNewRewardUnlockedService,
)
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class CreateChoreService:
    def __init__(
            self,
            chore_repository: ChoreRepository,
            recurring_chore_service: RecurringChoreService,
            save_user_points_service: SaveUserPointsService,
            detect_new_reward_unlocked_service: DetectNewRewardUnlockedService,
    ):
        self.__chore_repository = chore_repository
        self.__recurring_chore_service = recurring_chore_service
        self.__save_user_points_service = save_user_points_service
        self.__detect_new_reward_unlocked_service = detect_new_reward_unlocked_service

    @logging(show_args=True, show_return=True)
    def execute(self, dto: CreateChoreDTO, commit: bool = True) -> bool:
        try:
            return self.__run(dto, commit)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_SINGLE_CHORE_SERVICE_ERROR.code())

    def __run(self, dto: CreateChoreDTO, commit: bool) -> bool:
        should_commit = dto.completed is False and dto.is_recurring is False and commit
        entity = self.__insert_chore(dto, should_commit)
        if dto.is_recurring:
            should_commit = dto.completed is False and commit
            self.__insert_recurring_chore(entity, dto, should_commit)
        unlocked = self.__reward_unlock_if_completed(dto)
        return unlocked and dto.created_by_user_id == dto.assigned_to_user_id

    def __insert_chore(self, dto: CreateChoreDTO, commit: bool) -> ChoreEntity:
        return self.__chore_repository.insert(create_chore_dto=dto, commit=commit)

    def __insert_recurring_chore(
            self,
            entity: ChoreEntity,
            dto: CreateChoreDTO,
            commit: bool
    ) -> None:
        recurring_dto = RecurringChoreDTO(
            family_id=dto.family_id,
            chore_id=entity.id,
            day_of_the_week_ids=dto.recurrence_day_ids,
            is_recurring=dto.is_recurring,
            is_chore_completed=dto.completed,
        )
        self.__recurring_chore_service.execute(dto=recurring_dto, commit=commit)

    def __reward_unlock_if_completed(self, dto: CreateChoreDTO) -> bool:
        if not dto.completed or dto.assigned_to_user_id is None:
            return False
        check = self.__detect_new_reward_unlocked_service.execute(
            user_id=dto.assigned_to_user_id,
            mutate_points=lambda: self.__add_points(dto),
        )
        return check.new_reward_unlocked

    def __add_points(self, dto: CreateChoreDTO) -> None:
        points_dto = AddUserPointsDTO(
            user_id=dto.assigned_to_user_id,
            points=dto.points,
            family_id=dto.family_id,
        )
        self.__save_user_points_service.execute(dto=points_dto)
