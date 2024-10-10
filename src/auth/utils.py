import re
from datetime import datetime, timedelta
from typing import Any, Dict

import bcrypt
import jwt

from src.auth.config import auth_config
from src.auth.constants import user_data_validation
from src.auth.security import password_policy
from src.utils.rsa_keys_manager import keys_manager


def username_check(
    username: str,
) -> bool:
    return not (
        len(username) == 0
        or len(username) > user_data_validation.MAX_LEN_LOGIN
        or ' ' in username
    )


def password_check(
    password: str,
) -> bool:
    return not (
        len(password) > user_data_validation.MAX_LEN_PASSWORD
        or password_policy.policy.test(password)
        or not bool(re.fullmatch(r'[A-Za-z0-9@#$%^&*!]+', password))
    )


def hash_password(password: str) -> bytes:
    """
    Хэшировать пароль с использованием bcrypt.

    Args:
        password (str): Пароль в виде строки.

    Returns:
        bytes: Зашифрованный пароль в виде байтов.
    """
    password_bytes = bytes(password, 'utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(
        password_bytes,
        salt,
    )


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    """
    Проверить, соответствует ли введенный пароль зашифрованному паролю.

    Args:
        password (str): Пароль в виде строки.
        hashed_password (bytes): Хешированный пароль в виде байтов.

    Returns:
        bool: Результат проверки пароля.
    """
    password_bytes = bytes(password, 'utf-8')

    return bcrypt.checkpw(
        password_bytes,
        hashed_password,
    )


def encode_jwt(
        payload: Dict[str, Any],
        expiration_time: timedelta,
) -> str:
    """
    Кодировать данные в JWT токен с указанным временем действия.

    Args:
        payload (Dict[str, Any]): Payload для токена.
        expiration_time (timedelta): Время действия токена.

    Returns:
        str: Сформированный JWT токен.
    """
    to_encode = payload.copy()
    utc_now = datetime.utcnow()
    exp = utc_now + expiration_time
    to_encode.update(
        iat=utc_now,
        exp=exp,
    )

    return jwt.encode(
        payload=to_encode,
        key=keys_manager.get_private_key,
        algorithm=auth_config.algorithm,
    )


def decode_jwt(
        token: str | bytes,
) -> Dict[str, Any]:
    """
    Декодировать JWT токен и получить его payload.

    Args:
        token (str | bytes): JWT токен для декодирования.

    Returns:
        Dict[str, Any]: Payload токена.
    """
    return jwt.decode(
        jwt=token,
        key=keys_manager.get_public_key,
        algorithms=[auth_config.algorithm],
    )
