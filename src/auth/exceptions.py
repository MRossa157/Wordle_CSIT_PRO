from fastapi import HTTPException, status
from starlette.datastructures import MutableHeaders


class HTTP400BadRequest(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class HTTP401Unauthorized(HTTPException):
    def __init__(
            self,
            detail: str,
            headers: MutableHeaders | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )
