from sqlalchemy.orm import Session

from src.application.schemas.chores.create_chore_dto import CreateChoreDTO
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
        )
        self.db_session.add(model)
        if commit:
            self.db_session.flush()
            self.db_session.commit()
        else:
            self.db_session.flush()
        return model.to_entity()

    def find_by_family_id(self, family_id: int) -> list[ChoreEntity]:
        models: list[ChoreModel] | None = (
            self.db_session.query(ChoreModel)
            .filter_by(family_id=family_id)
            .order_by(ChoreModel.id)
            .all()
        )
        return [m.to_entity() for m in models] if models else []

    def find_by_id(self, chore_id: int, family_id: int) -> ChoreEntity | None:
        model: ChoreModel | None = (
            self.db_session.query(ChoreModel).filter_by(id=chore_id, family_id=family_id).first())

        return model.to_entity() if model else None

    def update(self, chore_id: int, family_id: int, update_chore_dto: UpdateChoreDTO,
               commit: bool = True) -> ChoreEntity:
        model: ChoreModel | None = self.db_session.query(ChoreModel).filter_by(id=chore_id, family_id=family_id).first()

        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.CHORE_NOT_FOUND.code())

        model.title = update_chore_dto.title
        model.emoji = update_chore_dto.emoji
        model.points = update_chore_dto.points
        model.assigned_to_user_id = update_chore_dto.assigned_to_user_id
        model.completed = update_chore_dto.completed

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
