from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.core.security import (
    get_password_hash, verify_password, create_access_token, get_current_user
)
from app.repositories.user_repo import get_user_by_email, create_user
from app.schemas.auth import UserCreate, UserOut, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

# Register a new user
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = await create_user(db, payload.email, get_password_hash(payload.password))
    return user

# Login existing user
@router.post("/login", response_model=Token)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        # Always 401 for bad credentials
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user.id)
    return Token(access_token=token)