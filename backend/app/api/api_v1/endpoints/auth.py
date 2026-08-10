from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str

fake_users_db = {
    'student@example.com': {
        'username': 'student@example.com',
        'hashed_password': pwd_context.hash('password123'),
    }
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = fake_users_db.get(username)
    if not user:
        return None
    user_obj = UserInDB(**user)
    if not verify_password(password, user_obj.hashed_password):
        return None
    return user_obj

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

@router.get('/me')
def read_users_me(token: str = Depends(oauth2_scheme)) -> dict[str, str]:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {'username': username}
