from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.security.auth import decode_token


async def get_current_user(token: str, db: AsyncSession) -> User | None:
    payload = decode_token(token)
    if payload is None:
        return None

    user_id = payload.get("sub")
    if user_id is None:
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_current_active_user(token: str, db: AsyncSession) -> User | None:
    user = await get_current_user(token, db)
    if user and user.is_active:
        return user
    return None
