from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()


def _authenticate_and_issue_token(email: str, password: str, db: Session) -> TokenResponse:
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    return _authenticate_and_issue_token(credentials.email, credentials.password, db)


@router.post("/token", response_model=TokenResponse)
def token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2 password flow uses "username"; this app treats it as the user's email.
    return _authenticate_and_issue_token(form_data.username, form_data.password, db)
