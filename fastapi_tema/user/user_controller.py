from datetime import timedelta
from logging import getLogger
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import fastapi_tema.db.db_settings as settings
from .user_entity import User
from .user_model import DeleteUserResponse
from .user_model import ShowUser
from .user_model import Token
from .user_model import UpdatedUserResponse
from .user_model import UpdateUserRequest
from .user_model import UserCreate
from .user_service import _create_new_user
from .user_service import _delete_user
from .user_service import _get_user_by_id
from .user_service import _update_user
from .user_service import authenticate_user
from .user_service import check_user_permissions
from .user_service import get_current_user_from_token
from .utils import create_access_token
from fastapi_tema.db.db_session import get_db


#########################
# USER LOGIN CONTROLLER #
#########################


login_router = APIRouter()


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


########################
# USER MAIN CONTROLLER #
########################


logger = getLogger(__name__)

user_router = APIRouter()


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@user_router.delete("/", response_model=DeleteUserResponse)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> DeleteUserResponse:
    user_for_deletion = await _get_user_by_id(user_id, db)
    if user_for_deletion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if not check_user_permissions(
        target_user=user_for_deletion,
        current_user=current_user,
    ):
        raise HTTPException(status_code=403, detail="Forbidden.")
    deleted_user_id = await _delete_user(user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_router.patch("/admin_privilege", response_model=UpdatedUserResponse)
async def grant_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_promotion = await _get_user_by_id(user_id, db)
    if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
        raise HTTPException(
            status_code=409,
            detail=f"User with id {user_id} already promoted to admin / superadmin.",
        )
    if user_for_promotion is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_promotion.enrich_admin_roles_by_admin_role()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.delete("/admin_privilege", response_model=UpdatedUserResponse)
async def revoke_admin_privilege(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    if not current_user.is_superadmin:
        raise HTTPException(status_code=403, detail="Forbidden.")
    if current_user.user_id == user_id:
        raise HTTPException(
            status_code=400, detail="Cannot manage privileges of itself."
        )
    user_for_revoke_admin_privileges = await _get_user_by_id(user_id, db)
    if not user_for_revoke_admin_privileges.is_admin:
        raise HTTPException(
            status_code=409, detail=f"User with id {user_id} has no admin privileges."
        )
    if user_for_revoke_admin_privileges is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    updated_user_params = {
        "roles": user_for_revoke_admin_privileges.remove_admin_privileges_from_model()
    }
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)


@user_router.get("/", response_model=ShowUser)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> ShowUser:
    user = await _get_user_by_id(user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    return user


@user_router.patch("/", response_model=UpdatedUserResponse)
async def update_user_by_id(
    user_id: UUID,
    body: UpdateUserRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
) -> UpdatedUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail="At least one parameter for user update info should be provided",
        )
    user_for_update = await _get_user_by_id(user_id, db)
    if user_for_update is None:
        raise HTTPException(
            status_code=404, detail=f"User with id {user_id} not found."
        )
    if user_id != current_user.user_id:
        if check_user_permissions(
            target_user=user_for_update, current_user=current_user
        ):
            raise HTTPException(status_code=403, detail="Forbidden.")
    try:
        updated_user_id = await _update_user(
            updated_user_params=updated_user_params, session=db, user_id=user_id
        )
    except IntegrityError as err:
        logger.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    return UpdatedUserResponse(updated_user_id=updated_user_id)
