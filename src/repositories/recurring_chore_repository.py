from sqlalchemy.orm import Session, joinedload

from src.domain.entities.recurring_chore_entity import RecurringChoreEntity
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.repositories.models.recurring_chore_model import RecurringChoreModel


class RecurringChoreRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert_recurring_chores(self, dto: RecurringChoreDTO, commit: bool = True) -> None:
        if not dto.day_of_the_week_ids:
            return
        for day_of_the_week_id in dto.day_of_the_week_ids:
            model = RecurringChoreModel(
                chore_id=dto.chore_id,
                family_id=dto.family_id,
                day_of_week_id=day_of_the_week_id,
                parent_chore_id=dto.parent_chore_id,
            )
            self.db_session.add(model)
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def delete_by_chore_id(self, chore_id: int, family_id: int, commit: bool = True) -> None:
        models = (
            self.db_session.query(RecurringChoreModel)
            .filter_by(chore_id=chore_id, family_id=family_id)
            .all()
        )
        for model in models:
            self.db_session.delete(model)
        if commit and models:
            self.db_session.commit()
        elif models:
            self.db_session.flush()

    def find_by_parent_chore_id_and_day(
        self, family_id: int, day_of_week_id: int
    ) -> list[RecurringChoreEntity]:
        models: list[RecurringChoreModel] = (
            self.db_session.query(RecurringChoreModel)
            .options(joinedload(RecurringChoreModel.day_of_week))
            .filter(
                RecurringChoreModel.family_id == family_id,
                RecurringChoreModel.day_of_week_id == day_of_week_id,
            )
            .all()
        )
        return [m.to_entity() for m in models]

    def find_chore_ids_done_for_day(
        self, family_id: int, day_of_week_id: int
    ) -> list[int]:
        """Chore IDs das cópias já feitas no dia (parent_chore_id preenchido)."""
        rows = (
            self.db_session.query(RecurringChoreModel.chore_id)
            .filter(
                RecurringChoreModel.family_id == family_id,
                RecurringChoreModel.day_of_week_id == day_of_week_id,
                RecurringChoreModel.parent_chore_id.isnot(None),
            )
            .all()
        )
        return [r[0] for r in rows]

    def find_by_chore_id_and_day(
        self, chore_id: int, day_of_week_id: int, family_id: int
    ) -> RecurringChoreEntity | None:
        model = (
            self.db_session.query(RecurringChoreModel)
            .options(joinedload(RecurringChoreModel.day_of_week))
            .filter(
                RecurringChoreModel.family_id == family_id,
                RecurringChoreModel.day_of_week_id == day_of_week_id,
                RecurringChoreModel.chore_id == chore_id,
            )
            .first()
        )
        return model.to_entity() if model else None
