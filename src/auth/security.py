from typing import Dict, Optional

from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from password_strength import PasswordPolicy

from src.auth.exceptions import HTTP401Unauthorized


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        token_url: str,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ) -> None:
        if not scopes:
            scopes = {}

        flows = OAuthFlowsModel(
            password={
                'tokenUrl': token_url,
                'scopes': scopes,
            },
        )
        super().__init__(
            flows=flows,
            auto_error=auto_error,
        )

    async def __call__(
        self,
        request: Request,
        token_type: Optional[str] = None,
    ) -> Optional[str]:
        authorization: str = request.cookies.get(token_type)
        if not authorization:
            if self.auto_error:
                raise HTTP401Unauthorized(detail='Not authenticated')
            return None

        return authorization


class _Policy:
    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=1,
        numbers=1,
        special=0,
        nonletters=0,
    )


password_policy = _Policy()
