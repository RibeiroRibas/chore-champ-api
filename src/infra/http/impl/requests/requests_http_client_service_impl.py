from typing import Optional, TypeVar, Generic, override

import requests

from src.domain.errors.internal_error import InternalError
from src.infra.http.errors.codes.infra_error_codes import InfraErrorCodes
from src.infra.http.errors.http_client_error import HttpClientError
from src.infra.http.i_http_client_service import IHttpClientService
from src.infra.http.responses.http_body import HttpBody
from src.infra.http.responses.http_files import HttpFiles
from src.infra.http.responses.http_headers import HttpHeaders
from src.infra.http.responses.http_params import HttpParams
from src.infra.http.responses.http_response import HttpResponse
from src.domain.errors.codes.internal_error_codes import InternalErrorCodes

T = TypeVar('T')

class RequestsHttpClientServiceImpl(IHttpClientService[T], Generic[T]):
    def __init__(
            self,
            timeout: int = 30,
            verify_ssl: bool = True,
            default_headers: Optional[HttpHeaders] = None
    ):
        self.__timeout = timeout
        self.__verify_ssl = verify_ssl
        self.__session = requests.Session()
        self.__default_headers = default_headers or HttpHeaders()

    @override
    def post(
            self,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None,
            files: Optional[HttpFiles] = None
    ) -> HttpResponse[T]:
        return self.request("POST", url, body, headers, params, files)

    @override
    def get(
            self,
            url: str,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        return self.request("GET", url, None, headers, params)

    @override
    def put(
            self,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        return self.request("PUT", url, body, headers, params)

    @override
    def delete(
            self,
            url: str,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None
    ) -> HttpResponse[T]:
        return self.request("DELETE", url, None, headers, params)

    @override
    def request(
            self,
            method: str,
            url: str,
            body: Optional[HttpBody] = None,
            headers: Optional[HttpHeaders] = None,
            params: Optional[HttpParams] = None,
            files: Optional[HttpFiles] = None
    ) -> HttpResponse[T]:
        try:
            merged_headers = self.__merge_headers(headers)

            response = self.__session.request(
                method=method,
                url=url,
                headers=merged_headers.to_dict(),
                json=body.to_dict() if body else None,
                timeout=self.__timeout,
                verify=self.__verify_ssl,
                params=params.to_dict() if params else None,
                files=files.to_dict() if files else None,
            )

            http_response = HttpResponse(
                data=response.json() if response.content else None,
                status_code=response.status_code,
                status_message=response.reason,
                text=response.text,
                headers=dict(response.headers)
            )

            if http_response.has_error():
                raise HttpClientError(
                    status_code=response.status_code,
                    response=http_response
                )

            return http_response
        except requests.exceptions.Timeout:
            raise InternalError(
                code=InfraErrorCodes.HTTP_CLIENT_TIMEOUT_ERROR.code()
            )
        except requests.exceptions.SSLError:
            raise InternalError(
                code=InfraErrorCodes.HTTP_CLIENT_SSL_ERROR.code()
            )
        except requests.exceptions.ConnectionError:
            raise InternalError(
                code=InfraErrorCodes.HTTP_CLIENT_CONNECTION_ERROR.code()
            )
        except requests.exceptions.RequestException:
            raise InternalError(
                code=InfraErrorCodes.HTTP_CLIENT_REQUEST_ERROR.code()
            )
        except HttpClientError:
            raise
        except Exception:
            raise InternalError(
                code=InfraErrorCodes.HTTP_CLIENT_UNEXPECTED_ERROR.code()
            )

    def __merge_headers(self, headers: HttpHeaders | None) -> HttpHeaders:
        merged_headers = HttpHeaders()
        merged_headers.merge(self.__default_headers)
        if headers:
            merged_headers.merge(headers)
        return merged_headers
