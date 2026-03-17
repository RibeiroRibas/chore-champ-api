from sqlalchemy.orm import Session

from src.application.schemas.chores.create_chore_dto import CreateChoreDTO
from src.application.schemas.chores.get_chores_filtered_dto import (
    GetChoresFilteredDto,
)
from src.application.schemas.chores.get_paginated_chores_dto import (
    GetPaginatedChoresDto,
)
from src.application.schemas.chores.update_chore_dto import UpdateChoreDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.chore_user_entity import ChoreUserEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.models.chore_model import ChoreModel


class ChoreRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, create_chore_dto: CreateChoreDTO, commit: bool = True) -> ChoreEntity:
        model = ChoreModel(
            family_id=create_chore_dto.family_id,
            title=create_chore_dto.title,
            emoji=create_chore_dto.emoji,
            points=create_chore_dto.points,
            assigned_to_user_id=create_chore_dto.assigned_to_user_id,
            created_by_user_id=create_chore_dto.created_by_user_id,
            completed=create_chore_dto.completed,
            is_recurring=create_chore_dto.is_recurring,
        )
        self.db_session.add(model)
        self.db_session.flush()

        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()
        return model.to_entity()


    def find_by_family_id(self, family_id: int, limit: int = 30) -> list[ChoreEntity]:
        models: list[ChoreModel] | None = (
            self.db_session.query(ChoreModel)
            .filter_by(family_id=family_id)
            .order_by(ChoreModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return [m.to_entity() for m in models] if models else []

    def find_paginated(
        self,
        family_id: int,
        dto: GetChoresFilteredDto,
    ) -> GetPaginatedChoresDto:
        query = self.db_session.query(ChoreModel).filter_by(family_id=family_id)
        if dto.completed is not None:
            query = query.filter(ChoreModel.completed == dto.completed)
        if dto.is_recurring is not None:
            query = query.filter(ChoreModel.is_recurring == dto.is_recurring)
        if dto.title is not None and dto.title.strip():
            query = query.filter(
                ChoreModel.title.ilike(f"%{dto.title.strip()}%")
            )
        if dto.assigned_to_user_id is not None:
            query = query.filter(ChoreModel.assigned_to_user_id == dto.assigned_to_user_id)
        total = query.count()
        models: list[ChoreModel] = (
            query.order_by(ChoreModel.created_at.desc())
            .offset((dto.page - 1) * dto.page_size)
            .limit(dto.page_size)
            .all()
        )
        items = [m.to_entity() for m in models]
        return GetPaginatedChoresDto(
            items=items,
            total_items=total,
            page=dto.page,
            page_size=dto.page_size,
            total_pages=(total + dto.page_size - 1) // dto.page_size,
        )

    def find_by_id(self, chore_id: int, family_id: int) -> ChoreEntity | None:
        model: ChoreModel | None = (
            self.db_session.query(ChoreModel).filter_by(id=chore_id, family_id=family_id).first())

        return model.to_entity() if model else None

    def update(self, chore_id: int, family_id: int, update_chore_dto: UpdateChoreDTO, commit: bool = True) -> ChoreEntity:
        model: ChoreModel | None = self.db_session.query(ChoreModel).filter_by(id=chore_id, family_id=family_id).first()

        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.CHORE_NOT_FOUND.code())

        model.title = update_chore_dto.title
        model.emoji = update_chore_dto.emoji
        model.points = update_chore_dto.points
        model.assigned_to_user_id = update_chore_dto.assigned_to_user_id
        model.completed = update_chore_dto.completed
        model.is_recurring = update_chore_dto.is_recurring

        self.db_session.merge(model)

        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()

        return model.to_entity()

    def delete_by_id(self, chore_id: int, family_id: int, commit: bool = True):
        model = (self.db_session.query(ChoreModel).filter_by(id=chore_id, family_id=family_id).first())

        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.CHORE_NOT_FOUND.code())

        self.db_session.delete(model)

        if commit:
            self.db_session.commit()

    def find_by_id_with_user(self, chore_id: int, family_id: int) -> ChoreUserEntity:
        model: ChoreModel | None = (
            self.db_session.query(ChoreModel)
            .filter_by(id=chore_id, family_id=family_id)
            .first()
        )

        return model.to_chore_user_entity() if model else None

    def exists_incomplete_copy_for_template_and_day(
        self, parent_recurring_chore_id: int, recurrence_day_of_week_id: int
    ) -> bool:
        return (
            self.db_session.query(ChoreModel.id)
            .filter(
                ChoreModel.parent_recurring_chore_id == parent_recurring_chore_id,
                ChoreModel.recurrence_day_of_week_id == recurrence_day_of_week_id,
                ChoreModel.completed.is_(False),
            )
            .first()
            is not None
        )

    def insert_copy(self, source_entity: ChoreEntity, commit: bool = True) -> ChoreEntity:
        new_model = ChoreModel(
            family_id=source_entity.family_id,
            title=source_entity.title,
            emoji=source_entity.emoji,
            points=source_entity.points,
            assigned_to_user_id=source_entity.assigned_to_user_id,
            created_by_user_id=source_entity.created_by_user_id,
            completed=False,
            is_recurring=source_entity.is_recurring
        )
        self.db_session.add(new_model)
        self.db_session.flush()
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()
        return new_model.to_entity()
