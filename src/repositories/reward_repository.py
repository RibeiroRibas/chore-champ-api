from sqlalchemy.orm import Session

from src.application.schemas.rewards.create_reward_dto import CreateRewardDTO
from src.application.schemas.rewards.update_reward_dto import UpdateRewardDTO
from src.domain.entities.reward_entity import RewardEntity
from src.domain.errors.codes.not_found_error_codes import NotFoundErrorCodes
from src.domain.errors.not_found_error import NotFoundError
from src.repositories.models.reward_model import RewardModel


class RewardRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def insert(self, dto: CreateRewardDTO, commit: bool = True) -> RewardEntity:
        model = RewardModel(
            title=dto.title,
            subtitle=dto.subtitle,
            emoji=dto.emoji,
            achievement_id=dto.achievement_id,
        )
        self.db_session.add(model)
        self.db_session.flush()
        if commit:
            self.db_session.commit()
            self.db_session.refresh(model)
        return model.to_entity()

    def find_all(self) -> list[RewardEntity]:
        models: list[RewardModel] = (
            self.db_session.query(RewardModel).order_by(RewardModel.id.asc()).all()
        )
        return [model.to_entity() for model in models]

    def find_by_id(self, reward_id: int) -> RewardEntity | None:
        model: RewardModel | None = (
            self.db_session.query(RewardModel).filter_by(id=reward_id).first()
        )
        return model.to_entity() if model else None

    def update(self, reward_id: int, dto: UpdateRewardDTO, commit: bool = True) -> RewardEntity:
        model: RewardModel | None = (
            self.db_session.query(RewardModel).filter_by(id=reward_id).first()
        )
        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.REWARD_NOT_FOUND.code())

        model.title = dto.title
        model.subtitle = dto.subtitle
        model.emoji = dto.emoji
        model.achievement_id = dto.achievement_id
        self.db_session.merge(model)
        if commit:
            self.db_session.commit()
            self.db_session.refresh(model)
        return model.to_entity()

    def delete_by_id(self, reward_id: int, commit: bool = True) -> None:
        model: RewardModel | None = (
            self.db_session.query(RewardModel).filter_by(id=reward_id).first()
        )
        if model is None:
            raise NotFoundError(code=NotFoundErrorCodes.REWARD_NOT_FOUND.code())
        self.db_session.delete(model)
        if commit:
            self.db_session.commit()
