import logging
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate
from app.schemas.token import AccessTokenResponse, RefreshTokenResponse
from app.services.auth_service import AuthService
from app.db.session import get_db
from app.core.security import decode_token

router = APIRouter()
logger = logging.getLogger("app.api.v1.auth")

@router.post("/register", response_model=AccessTokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.create_user(email=user_in.email, password=user_in.password)
    tokens = service.generate_tokens(user)
    # Set HttpOnly cookies
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, secure=False, samesite="lax")
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, secure=False, samesite="lax")
    return {"access_token": tokens["access_token"], "token_type": "bearer"}

@router.post("/login", response_model=AccessTokenResponse)
async def login(user_in: UserCreate, response: Response, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.authenticate_user(email=user_in.email, password=user_in.password)
    tokens = service.generate_tokens(user)
    response.set_cookie(key="access_token", value=tokens["access_token"], httponly=True, secure=False, samesite="lax")
    response.set_cookie(key="refresh_token", value=tokens["refresh_token"], httponly=True, secure=False, samesite="lax")
    return {"access_token": tokens["access_token"], "token_type": "bearer"}

@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        # Check revocation
        service = AuthService(db)
        if await service.is_token_revoked(payload.get("jti")):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
        # Issue new access token
        user_id = int(payload.get("sub"))
        email = payload.get("email")
        access_token = create_access_token({"sub": str(user_id), "email": email})
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as exc:
        logger.error("Refresh token error: %s", exc)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        payload = decode_token(refresh_token)
        jti = payload.get("jti")
        service = AuthService(db)
        await service.revoke_refresh_token(jti)
    # Clear cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
