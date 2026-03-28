from datetime import datetime

from sqlalchemy.orm import Session

from src.domain.schemas.dto.chores.recurring_chore_dto import RecurringChoreDTO
from src.domain.schemas.entity.recurring_chore_entity import RecurringChoreEntity
from src.repositories.models.recurring_chore_model import RecurringChoreModel


class RecurringChoreRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert_recurring_chores(self, dto: RecurringChoreDTO, commit: bool = True) -> None:
        if not dto.day_of_the_week_ids:
            return
        current_week_day: int = datetime.today().weekday() + 1
        for day_of_the_week_id in dto.day_of_the_week_ids:
            model = RecurringChoreModel(
                chore_id=dto.chore_id,
                family_id=dto.family_id,
                day_of_week_id=day_of_the_week_id,
                completed_at=datetime.now() if current_week_day == day_of_the_week_id and dto.is_chore_completed else None,
            )
            self.db_session.add(model)
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def delete_by_day_of_the_week_ids(self, chore_id: int, day_of_the_week_ids: list[int], family_id: int,
                                      commit: bool = True):
        if not day_of_the_week_ids:
            return
        q = (
            self.db_session.query(RecurringChoreModel)
            .filter(
                RecurringChoreModel.chore_id == chore_id,
                RecurringChoreModel.family_id == family_id,
                RecurringChoreModel.day_of_week_id.in_(day_of_the_week_ids),
            )
        )
        q.delete(synchronize_session=False)
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def find_by_chore_id(self, chore_id: int, family_id: int) -> list[RecurringChoreEntity] | None:
        rows: list[RecurringChoreModel] = (self.db_session.query(RecurringChoreModel)
                                           .filter_by(chore_id=chore_id)
                                           .filter_by(family_id=family_id)
                                           .all())
        return [row.to_entity() for row in rows] if rows else None

    def update_to_complete_by_day_of_week_id(self, chore_id: int, family_id: int, day_of_the_week_id: int,
                                             commit: bool = True):
        model: RecurringChoreModel | None = (self.db_session.query(RecurringChoreModel)
                                             .filter_by(chore_id=chore_id)
                                             .filter_by(family_id=family_id)
                                             .filter_by(day_of_week_id=day_of_the_week_id)
                                             .first())

        if not model:
            return

        model.completed_at = datetime.now()
        self.db_session.merge(model)

        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()

    def delete_by_chore_id(self, chore_id: int, family_id: int, commit: bool = True):
        q = (
            self.db_session.query(RecurringChoreModel)
            .filter(
                RecurringChoreModel.family_id == family_id,
                RecurringChoreModel.chore_id == chore_id,
            )
        )
        q.delete(synchronize_session=False)
        if commit:
            self.db_session.commit()
        else:
            self.db_session.flush()
