from enum import Enum

from src.domain.errors.models.error_model import ErrorModel


class BaseErrorCode(Enum):

    def code(self):
        return self.value[0]

    def message(self):
        return self.value[1]
