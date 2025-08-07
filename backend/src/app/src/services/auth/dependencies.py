from fastapi import Depends, HTTPException, Request, status

from backend.src.app.src.services.users.models import UserModel
from backend.src.app.src.services.users.repository import (
    UserRepository,
    inject_user_repository,
)


async def get_current_user(
    request: Request,
    user_repository: UserRepository = Depends(inject_user_repository),
) -> UserModel:
    """
    Dependency to get the current user from the session.
    It checks for a 'user_id' in the session, retrieves the user from the
    database, and raises an HTTPException if the user is not authenticated
    or not found.

    Args:
        request: The FastAPI Request object, used to access session data.
        user_repository: The injected UserRepository for database access.

    Returns:
        The UserModel object of the currently authenticated user.

    Raises:
        HTTPException:
            - 401 Unauthorized if no user_id is found in the session.
            - 401 Unauthorized if the user associated with the user_id is not found in the database.
    """
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id_uuid = user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session user ID format",
        )

    user = user_repository.find_by_id(user_id_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found, please log in again",
        )

    return user
