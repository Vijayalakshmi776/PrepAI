from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, decode_access_token, verify_password
from app.db.session import get_db
from app.schemas.user import Token, UserCreate, UserLogin, UserRead, UserRegister
from app.services.user import user_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_PREFIX}/auth/token')


def authenticate_user(db: Session, email: str, password: str):
    user = user_service.get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = decode_access_token(token)
        user_id: str | None = payload.get('sub')
        if user_id is None:
            raise credentials_exception
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token has expired',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except JWTError:
        raise credentials_exception
    user = user_service.get(db, user_id)
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Inactive user',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user


@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    normalized_email = user_in.email.lower()
    existing_user = user_service.get_by_email(db, normalized_email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')
    user_create = UserCreate(
        email=normalized_email,
        full_name=user_in.full_name,
        password=user_in.password,
    )
    user = user_service.create(db, user_create)
    return user


@router.post('/token', response_model=Token)
@router.post('/login', response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    normalized_email = user_in.email.lower()
    user = authenticate_user(db, normalized_email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Inactive user',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token = create_access_token(data={'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/me', response_model=UserRead)
def read_current_user(current_user=Depends(get_current_user)):
    return current_user
