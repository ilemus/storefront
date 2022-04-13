from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from storefront.config import settings
from storefront.models.person import Person, get_person_by_email

ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def authenticate_user(cursor, username: str, password: str) -> bool:
    """
    I think the return type is supposed to be an instance of person with person_id and person_email
    :param cursor:
    :param username:
    :param password:
    :return: boolean
    """
    # TODO: Can do a join table here
    cursor.execute('SELECT person_id from person where person_email=%s', (username,))
    person_id = cursor.fetchone()
    if person_id is None:
        return False
    person_id = int(person_id[0])
    cursor.execute('SELECT password from person_login where person_id=%s', (person_id,))
    current_password = cursor.fetchone()
    if current_password is None:
        return False
    current_password = current_password[0]
    return pwd_context.verify(secret=password, hash=current_password)


# This part is confusing
async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


async def get_current_active_user(current_user: str = Depends(get_current_user_email)):
    # Maybe add a Depends on request state to get more info, otherwise don't really care
    if current_user is None:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
# This part is confusing


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


@oauth2_router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if not settings.connect_to_database:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Not connected to database",
                            headers={"WWW-Authenticate": "Bearer"})
    cursor = request.state.sql_conn.cursor()
    user = authenticate_user(cursor, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
