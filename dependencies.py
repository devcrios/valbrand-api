from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from database import SessionLocal
from settings import settings
from sqlalchemy.orm import Session

api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API key")
    return api_key


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()