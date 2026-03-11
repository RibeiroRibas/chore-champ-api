from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.errors.bad_request_error import BadRequestError
from src.domain.errors.codes.bad_request_error_codes import BadRequestErrorCode


@dataclass(frozen=True, slots=True)
class PhoneVO:
    _digits: str

    def __post_init__(self) -> None:
        if not self._digits.isdigit():
            raise BadRequestError(code=BadRequestErrorCode.INVALID_PHONE.code())

        n = len(self._digits)
        if n not in (8, 9, 10, 11, 12, 13):
            raise BadRequestError(code=BadRequestErrorCode.INVALID_PHONE.code())

    @staticmethod
    def normalize(value: str) -> str:
        if value is None:
            raise BadRequestError(code=BadRequestErrorCode.INVALID_PHONE.code())
        digits = re.sub(r"\D+", "", str(value))
        if not digits:
            raise BadRequestError(code=BadRequestErrorCode.INVALID_PHONE.code())
        return digits

    @classmethod
    def from_raw(cls, value: str) -> "PhoneVO":
        return cls(cls.normalize(value))

    @property
    def digits(self) -> str:
        return self._digits

    @property
    def has_ddi(self) -> bool:
        return len(self._digits) in (12, 13)

    @property
    def has_ddd(self) -> bool:
        return len(self._digits) in (10, 11, 12, 13)

    @property
    def is_mobile(self) -> bool:
        return len(self._digits) in (9, 11, 13)

    @property
    def is_landline(self) -> bool:
        return len(self._digits) in (8, 10, 12)

    def formatted(self) -> str:
        d = self._digits
        n = len(d)

        if n == 8:   # ####-####
            return f"{d[:4]}-{d[4:]}"
        if n == 9:   # #####-####
            return f"{d[:5]}-{d[5:]}"
        if n == 10:  # (##) ####-####
            return f"({d[:2]}) {d[2:6]}-{d[6:]}"
        if n == 11:  # (##) #####-####
            return f"({d[:2]}) {d[2:7]}-{d[7:]}"
        if n == 12:  # +## (##) ####-####
            return f"+{d[:2]} ({d[2:4]}) {d[4:8]}-{d[8:]}"
        if n == 13:  # +## (##) #####-####
            return f"+{d[:2]} ({d[2:4]}) {d[4:9]}-{d[9:]}"
        raise BadRequestError(code=BadRequestErrorCode.INVALID_PHONE.code())

    def __str__(self) -> str:
        return self.formatted()
