from src.domain.errors.models.base_error_code import BaseErrorCode


class InfraErrorCodes(BaseErrorCode):
    UNPROCESSABLE_ENTITY = (422000, "Unprocessable Entity")

    INVALID_TOKEN = (401000, "Token inválido.")
    EXPIRED_TOKEN = (401001, "Token expirado.")
    MISSING_AUTHORIZATION_TOKEN = (401002, "Token de autorização ausente.")
    INVALID_SIGNATURE = (401003, "Assinatura inválida no token de autorização.")

    UNMAPPED_ERROR = (500000, "Unmapped internal error")
    HTTP_CLIENT_TIMEOUT_ERROR = (500001, "Timeout connecting to HTTP endpoint.")
    HTTP_CLIENT_SSL_ERROR = (500002, "SSL/TLS error connecting to HTTP endpoint.")
    HTTP_CLIENT_CONNECTION_ERROR = (500003, "Connection error with HTTP endpoint.")
    HTTP_CLIENT_REQUEST_ERROR = (500004, "Generic request error with HTTP endpoint.")
    HTTP_CLIENT_UNEXPECTED_ERROR = (500005, "An unexpected error occurred during HTTP request.")
    HTTP_CLIENT_EXTERNAL_DATA_ERROR = (500006, "External data error during HTTP request.")
    SEND_EMAIL_ERROR = (500007, "Send email error")
    RENDER_TEMPLATE_ERROR = (500008, "Render template error")
    ENCRYPTION_KEY_ERROR = (500009, "Encryption key error")
