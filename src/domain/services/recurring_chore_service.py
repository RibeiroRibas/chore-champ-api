from datetime import date

from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.entity.recurring_chore_entity import RecurringChoreEntity
from src.infra.decorators.logger import logging
from src.repositories.recurring_chore_repository import RecurringChoreRepository


class RecurringChoreService:
    def __init__(self, recurring_chore_repository: RecurringChoreRepository):
        self.recurring_chore_repository = recurring_chore_repository

    @logging(show_args=True, show_return=True)
    def execute(self, dto: RecurringChoreDTO, commit: bool = True):
        try:
            self.__execute(dto=dto, commit=commit)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.RECURRING_CHORE_SERVICE_ERROR.code())

    def __execute(self, dto: RecurringChoreDTO, commit: bool):
        if dto.should_delete():
            self.recurring_chore_repository.delete_by_chore_id(dto.chore_id, dto.family_id, commit)
            return

        current_week_day: int = date.today().weekday() + 1
        if dto.is_chore_completed and not dto.verify_day_match(current_week_day):
            raise BadRequestError(code=BadRequestErrorCode.RECURRING_CHORE_CAN_ONLY_BE_COMPLETED_TODAY.code())

        entities_from_db: list[RecurringChoreEntity] | None = self.recurring_chore_repository.find_by_chore_id(
            dto.chore_id, dto.family_id)

        if entities_from_db is None or len(entities_from_db) == 0:
            self.recurring_chore_repository.insert_recurring_chores(dto=dto, commit=commit)
            return

        self.__process_save_recurring_chore(commit, current_week_day, dto, entities_from_db)

    def __process_save_recurring_chore(self, commit: bool, current_week_day: int, dto: RecurringChoreDTO,
                                       entities_from_db: list[RecurringChoreEntity]):
        day_of_the_week_ids_to_remove: list[int] = []
        day_of_the_week_ids_to_update: list[int] = []
        for entity_from_db in entities_from_db:
            if dto.verify_day_match(entity_from_db.day_of_week.id):
                day_of_the_week_ids_to_update.append(entity_from_db.day_of_week.id)
            else:
                day_of_the_week_ids_to_remove.append(entity_from_db.day_of_week.id)

        day_of_weeks_from_db: list[int] = [entity_from_db.day_of_week.id for entity_from_db in entities_from_db]
        day_of_the_week_ids_to_add: list[int] = dto.get_new_days_of_week(day_of_weeks_from_db)

        should_commit: bool = len(day_of_the_week_ids_to_remove) == 0 and len(
            day_of_the_week_ids_to_update) == 0 and commit
        if len(day_of_the_week_ids_to_add) > 0:
            self.__insert(day_of_the_week_ids_to_add, dto, should_commit)

        should_commit: bool = len(day_of_the_week_ids_to_update) == 0 and commit
        if len(day_of_the_week_ids_to_remove) > 0:
            self.recurring_chore_repository.delete_by_day_of_the_week_ids(dto.chore_id, day_of_the_week_ids_to_remove,
                                                                          dto.family_id,
                                                                          should_commit)

        if len(day_of_the_week_ids_to_update) > 0:
            self.__update(commit, current_week_day, dto)

    def __update(self, commit: bool, current_week_day: int, dto: RecurringChoreDTO):
        if dto.is_chore_completed:
            is_update_today_chore: bool = dto.verify_day_match(current_week_day)
            if is_update_today_chore:
                self.recurring_chore_repository.update_to_complete_by_day_of_week_id(dto.chore_id, dto.family_id,
                                                                                     current_week_day, commit)

    def __insert(self, day_of_the_week_ids_to_add: list[int], dto: RecurringChoreDTO, should_commit: bool):
        new_dto = dto.with_new_days(day_of_the_week_ids_to_add)
        self.recurring_chore_repository.insert_recurring_chores(dto=new_dto, commit=should_commit)
