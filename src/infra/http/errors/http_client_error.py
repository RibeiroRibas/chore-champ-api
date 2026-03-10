from typing import Optional

from src.domain.errors.base_error import BaseError
from src.infra.http.responses.http_response import HttpResponse


class HttpClientError(BaseError):
    def __init__(
        self,
        status_code: Optional[int] = None,
        response: Optional[HttpResponse] = None,
        code: Optional[int] = None
    ):
        super().__init__(code=code)
        self.status_code = status_code
        self.response = response
