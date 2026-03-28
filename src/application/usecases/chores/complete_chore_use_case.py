from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.create_chore_dto import CreateChoreDTO
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.dto.chores.update_chore_dto import UpdateChoreDTO
from src.domain.schemas.dto.users.add_user_points_dto import AddUserPointsDTO
from src.domain.schemas.entity.chore_entity import ChoreEntity
from src.domain.schemas.entity.current_user_entity import CurrentUserEntity
from src.domain.services.create_chore_service import CreateChoreService
from src.domain.services.detect_new_reward_unlocked_service import (
    DetectNewRewardUnlockedService,
)
from src.domain.services.get_chore_service import GetChoreService
from src.domain.services.list_today_chore_entities_service import (
    ListTodayChoreEntitiesService,
)
from src.domain.services.recurring_chore_service import RecurringChoreService
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository


class CompleteChoreUseCase:
    def __init__(
            self,
            chore_repository: ChoreRepository,
            get_chore_service: GetChoreService,
            recurring_chore_service: RecurringChoreService,
            save_user_points_service: SaveUserPointsService,
            list_today_chore_entities_service: ListTodayChoreEntitiesService,
            detect_new_reward_unlocked_service: DetectNewRewardUnlockedService,
            creat_chore_service: CreateChoreService,
    ):
        self.chore_repository = chore_repository
        self.get_chore_service = get_chore_service
        self.recurring_chore_service = recurring_chore_service
        self.save_user_points_service = save_user_points_service
        self.list_today_chore_entities_service = list_today_chore_entities_service
        self.detect_new_reward_unlocked_service = detect_new_reward_unlocked_service
        self.__creat_chore_service = creat_chore_service

    @logging(show_args=True, show_return=True)
    def execute(self, chore_id: int, current_user: CurrentUserEntity) -> bool:
        try:
            return self.__complete_chore(chore_id=chore_id, current_user=current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.COMPLETE_CHORE_ERROR.code())

    def __complete_chore(self, chore_id: int, current_user: CurrentUserEntity) -> bool:
        chore = self.__get_chore_by_id(chore_id, current_user)
        today_chores = self.list_today_chore_entities_service.execute(current_user.family_id)
        chore.validate_can_complete(current_user, today_chores)

        return self.__detect_new_reward_unlocked_and_complete_chores_and_update_points(chore, current_user)

    def __detect_new_reward_unlocked_and_complete_chores_and_update_points(self, chore: ChoreEntity,
                                                                           current_user: CurrentUserEntity) -> bool:
        new_reward_unlocked = self.detect_new_reward_unlocked_service.execute(
            user_id=chore.assigned_to_user_id,
            mutate_points=lambda: self.__apply_complete_chore_persistence(
                current_user=current_user,
                chore=chore,
            ),
        ).new_reward_unlocked
        return new_reward_unlocked and chore.assigned_to_user_id == current_user.user_id

    def __apply_complete_chore_persistence(
            self,
            current_user: CurrentUserEntity,
            chore: ChoreEntity,
    ) -> None:
        if chore.is_recurring:
            self.__handle_recurring_chore(current_user, chore)
        else:
            self.__update_chore(chore, current_user)
        self.__save_user_points(chore, current_user)

    def __get_chore_by_id(self, chore_id: int, current_user: CurrentUserEntity) -> ChoreEntity:
        chore: ChoreEntity = self.get_chore_service.execute(
            chore_id=chore_id,
            family_id=current_user.family_id,
        )

        return chore

    def __save_user_points(self, chore: ChoreEntity, current_user: CurrentUserEntity):
        points_dto = AddUserPointsDTO(
            user_id=chore.assigned_to_user_id,
            points=chore.points,
            family_id=current_user.family_id,
        )
        self.save_user_points_service.execute(dto=points_dto)

    def __handle_recurring_chore(self, current_user: CurrentUserEntity, chore: ChoreEntity):
        self.__update_recurring_chore(chore, current_user)
        self.__create_completed_chore_copy(chore)

    def __update_recurring_chore(self, chore: ChoreEntity, current_user: CurrentUserEntity):
        recurring_dto = RecurringChoreDTO(
            family_id=current_user.family_id,
            chore_id=chore.id,
            day_of_the_week_ids=[d.id for d in chore.recurrence_days],
            is_recurring=chore.is_recurring,
            is_chore_completed=True,
        )
        self.recurring_chore_service.execute(dto=recurring_dto, commit=False)

    def __create_completed_chore_copy(self, chore: ChoreEntity):
        create_chore_dto = CreateChoreDTO(
            family_id=chore.family_id,
            title=chore.title,
            emoji=chore.emoji,
            points=chore.points,
            created_by_user_id=chore.created_by_user_id,
            assigned_to_user_id=chore.assigned_to_user_id,
            completed=True,
        )
        self.__creat_chore_service.execute(dto=create_chore_dto, commit=False)

    def __update_chore(self, chore: ChoreEntity, current_user: CurrentUserEntity) -> ChoreEntity:
        dto = UpdateChoreDTO(
            title=chore.title,
            emoji=chore.emoji,
            points=chore.points,
            assigned_to_user_id=chore.assigned_to_user_id,
            completed=True,
            is_recurring=chore.is_recurring,
        )

        updated: ChoreEntity = self.chore_repository.update(
            chore_id=chore.id,
            family_id=current_user.family_id,
            update_chore_dto=dto,
            commit=False,
        )
        return updated
