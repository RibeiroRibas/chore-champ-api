from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

from src.infra.http.responses.http_body import HttpBody
from src.infra.http.responses.http_files import HttpFiles
from src.infra.http.responses.http_headers import HttpHeaders
from src.infra.http.responses.http_params import HttpParams
from src.infra.http.responses.http_response import HttpResponse

T = TypeVar('T')


class IHttpClientService(ABC, Generic[T]):

    @abstractmethod
    def post(
            self,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None,
            files: Optional[HttpFiles] = None,
    ) -> HttpResponse[T]:
        raise NotImplementedError("Method 'post' not implemented.")

    @abstractmethod
    def get(
            self,
            url: str,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        raise NotImplementedError("Method 'get' not implemented.")

    @abstractmethod
    def put(
            self,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        raise NotImplementedError("Method 'put' not implemented.")

    @abstractmethod
    def delete(
            self,
            url: str,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        raise NotImplementedError("Method 'delete' not implemented.")

    @abstractmethod
    def request(
            self,
            method: str,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None,
            files: Optional[HttpFiles] = None
    ) -> HttpResponse[T]:
        raise NotImplementedError("Method 'request' not implemented.")
