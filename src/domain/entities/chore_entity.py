from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode


class ChoreEntity:
    def __init__(
        self,
        chore_id: int,
        family_id: int,
        title: str,
        emoji: str,
        points: int,
        assigned_to_user_id: int | None,
        created_by_user_id: int,
        completed: bool,
    ):
        self.id = chore_id
        self.family_id = family_id
        self.title = title
        self.emoji = emoji
        self.points = points
        self.assigned_to_user_id = assigned_to_user_id
        self.created_by_user_id = created_by_user_id
        self.completed = completed


    def validate_can_update_or_delete(self):
        if self.completed:
           raise BadRequestError(code=BadRequestErrorCode.CANNOT_UPDATE_OR_DELETE_CHORE_AFTER_COMPLETED.code())
