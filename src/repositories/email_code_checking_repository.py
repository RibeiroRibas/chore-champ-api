from sqlalchemy import delete
from sqlalchemy.orm import Session

from src.application.schemas.create_email_code_checking_dto import CreateEmailCodeCheckingDTO
from src.domain.entities.email_code_checking_entity import EmailCodeCheckingEntity
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.repositories.models import EmailCodeCheckingModel


class EmailCodeCheckingRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def __insert(self, email_code_checking_dto: CreateEmailCodeCheckingDTO, commit: bool = True):
        email_code_checking = EmailCodeCheckingModel(email=email_code_checking_dto.email, code=email_code_checking_dto.code)
        self.db_session.add(email_code_checking)
        if commit:
            self.db_session.commit()

    def find_by_email(self, email: str) -> EmailCodeCheckingEntity | None:
        model: EmailCodeCheckingModel | None = self.db_session.query(EmailCodeCheckingModel).filter_by(email=email).first()
        return model.to_entity() if model else None

    def __delete_by_id(self, email_code_checking_id: int):
        stmt = delete(EmailCodeCheckingModel).where(EmailCodeCheckingModel.id == email_code_checking_id)
        self.db_session.execute(stmt)
        self.db_session.commit()

    def update(self, email_code_checking: EmailCodeCheckingEntity):
        model = EmailCodeCheckingModel.from_entity(email_code_checking)
        self.db_session.merge(model)
        self.db_session.commit()

    def delete_and_insert(self, email_code_checking_dto: CreateEmailCodeCheckingDTO):
        try:
            existing_email_code_checking = self.find_by_email(email=email_code_checking_dto.email)

            if existing_email_code_checking:
                self.__delete_by_id(existing_email_code_checking.id)

            self.__insert(email_code_checking_dto)
        except Exception:
            raise InternalError(code=InternalErrorCodes.CANNOT_PERSIST_EMAIL_CODE_ERROR.code())
