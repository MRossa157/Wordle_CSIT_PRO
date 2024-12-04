from fastapi import HTTPException, status
from starlette.datastructures import MutableHeaders


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
