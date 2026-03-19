from src.api.v1.requests.chores.create_chore_request import CreateChoreRequest
from src.api.v1.responses.chores.chore_response import ChoreResponse
from src.application.schemas.chores.create_chore_dto import CreateChoreDTO
from src.application.schemas.users.add_user_points_dto import AddUserPointsDTO
from src.domain.entities.chore_entity import ChoreEntity
from src.domain.entities.current_user_entity import CurrentUserEntity
from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.base_error import BaseError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes
from src.domain.errors.internal_error import InternalError
from src.domain.schemas.recurring_chore_dto import RecurringChoreDTO
from src.domain.services.save_user_points_service import SaveUserPointsService
from src.infra.decorators.logger import logging
from src.repositories.chore_repository import ChoreRepository
from src.repositories.recurring_chore_repository import RecurringChoreRepository


class CreateChoreUseCase:
    def __init__(
        self,
        chore_repository: ChoreRepository,
        recurring_chore_repository: RecurringChoreRepository,
        save_user_points_service: SaveUserPointsService,
    ):
        self.chore_repository = chore_repository
        self.recurring_chore_repository = recurring_chore_repository
        self.save_user_points_service = save_user_points_service


    @logging(show_args=True, show_return=True)
    def execute(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> ChoreResponse:
        try:
            return self.__process_create_chore(request, current_user)
        except Exception as error:
            if isinstance(error, BaseError):
                raise error
            raise InternalError(code=InternalErrorCodes.CREATE_CHORE_ERROR.code())

    def __process_create_chore(self, request: CreateChoreRequest, current_user: CurrentUserEntity) -> ChoreResponse:
        if request.is_recurring and (request.recurrence_day_ids is None or len(request.recurrence_day_ids) == 0):
            raise BadRequestError(code=BadRequestErrorCode.RECURRENCE_DAY_IDS_REQUIRED.code())

        entity = self.__create_chore(current_user, request)

        if request.is_recurring:
            should_commit = request.completed is False
            self.create_recurring_chore(current_user, entity, request, should_commit)

        if request.completed:
            self.__update_points(current_user, request)

        return ChoreResponse.from_entity(entity)

    def __create_chore(self, current_user: CurrentUserEntity, request: CreateChoreRequest) -> ChoreEntity:
        dto = CreateChoreDTO(
            family_id=current_user.family_id,
            title=request.title,
            emoji=request.emoji,
            points=request.points,
            created_by_user_id=current_user.user_id,
            assigned_to_user_id=request.assigned_to_user_id,
            completed=request.completed,
            is_recurring=request.is_recurring,
            recurrence_day_ids=request.recurrence_day_ids,
        )

        should_commit = request.is_recurring is False or request.completed is False
        entity: ChoreEntity = self.chore_repository.insert(create_chore_dto=dto, commit=should_commit)
        return entity

    def __update_points(self, current_user: CurrentUserEntity, request: CreateChoreRequest):
        points_dto = AddUserPointsDTO(
            user_id=request.assigned_to_user_id,
            points=request.points,
            family_id=current_user.family_id,
        )
        self.save_user_points_service.execute(points_dto)

    def create_recurring_chore(self, current_user: CurrentUserEntity, entity: ChoreEntity, request: CreateChoreRequest,
                               should_commit: bool):
        recurring_dto = RecurringChoreDTO(
            family_id=current_user.family_id,
            chore_id=entity.id,
            day_of_the_week_ids=request.recurrence_day_ids,
            is_recurring=request.is_recurring,
            is_chore_completed=request.completed
        )
        self.recurring_chore_repository.insert_recurring_chores(dto=recurring_dto, commit=should_commit)
        entity.recurrence_day_ids = request.recurrence_day_ids
