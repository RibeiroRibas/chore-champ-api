from src.domain.entities.chore_entity import ChoreEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.repositories.chore_repository import ChoreRepository
from src.repositories.recurring_chore_repository import RecurringChoreRepository


class RecurringChoreService:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        recurring_chore_repository: RecurringChoreRepository,
    ):
        self.chore_repository = chore_repository
        self.recurring_chore_repository = recurring_chore_repository

    def execute(self, dto: RecurringChoreDTO) -> None:
        if not dto.is_chore_completed:
            self.recurring_chore_repository.delete_by_chore_id(
                dto.chore_id, dto.family_id, commit=False
            )
            self.recurring_chore_repository.insert_recurring_chores(dto=dto)
            return

        chore_entity: ChoreEntity | None = self.chore_repository.find_by_id(
            dto.chore_id, dto.family_id
        )

        if chore_entity is None:
            raise NotFoundError(code=NotFoundErrorCodes.CHORE_NOT_FOUND.code())

        if (dto.is_recurring is not None and dto.is_recurring is True) or chore_entity.is_recurring is True:
            entity_copy: ChoreEntity = self.chore_repository.insert_copy(
                source_entity=chore_entity, commit=False
            )
            dto.chore_id = entity_copy.id
            dto.parent_chore_id = chore_entity.id
            self.recurring_chore_repository.insert_recurring_chores(dto=dto)

        self.recurring_chore_repository.delete_by_chore_id(
            chore_entity.id, dto.family_id
        )
