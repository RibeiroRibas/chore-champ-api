from src.domain.schemas.dto.chores.create_chore_dto import CreateChoreDTO
from src.domain.schemas.dto.users.add_user_points_dto import AddUserPointsDTO
from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.services.detect_new_reward_unlocked_service import (
    DetectNewRewardUnlockedService,
)
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository
from src.repositories.recurring_chore_repository import RecurringChoreRepository


class CreateChoreService:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        recurring_chore_repository: RecurringChoreRepository,
        save_user_points_service: SaveUserPointsService,
        detect_new_reward_unlocked_service: DetectNewRewardUnlockedService,
    ):
        self.__chore_repository = chore_repository
        self.__recurring_chore_repository = recurring_chore_repository
        self.__save_user_points_service = save_user_points_service
        self.__detect_new_reward_unlocked_service = detect_new_reward_unlocked_service

    @logging(show_args=True, show_return=True)
    def execute(self, dto: CreateChoreDTO) -> bool:
        try:
            return self.__run(dto)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_SINGLE_CHORE_SERVICE_ERROR.code())

    def __run(self, dto: CreateChoreDTO) -> bool:
        entity = self.__insert_chore(dto)
        if dto.is_recurring:
            self.__insert_recurring_chore(entity, dto)
        unlocked = self.__reward_unlock_if_completed(dto)
        return unlocked

    def __insert_chore(self, dto: CreateChoreDTO) -> ChoreEntity:
        should_commit = dto.is_recurring is False or dto.completed is False
        return self.__chore_repository.insert(create_chore_dto=dto, commit=should_commit)

    def __insert_recurring_chore(
        self,
        entity: ChoreEntity,
        dto: CreateChoreDTO,
    ) -> None:
        should_commit = dto.completed is False
        recurring_dto = RecurringChoreDTO(
            family_id=dto.family_id,
            chore_id=entity.id,
            day_of_the_week_ids=dto.recurrence_day_ids,
            is_recurring=dto.is_recurring,
            is_chore_completed=dto.completed,
        )
        self.__recurring_chore_repository.insert_recurring_chores(
            dto=recurring_dto,
            commit=should_commit,
        )

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
