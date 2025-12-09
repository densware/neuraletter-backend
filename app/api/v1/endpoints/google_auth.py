from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.core.config import settings
from app.db.session import get_db
from app.services import google_auth_service

router = APIRouter()


# Pydantic models for structured responses
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)


# Step 1: Redirect user to Google login
@router.get("/google/login")
async def login(request: Request):
    try:
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        return JSONResponse(content={"message":"Login with google failed", "error": str(e)}, status_code=500)


# Step 2: Callback endpoint
@router.get("/google/callback", response_model=TokenResponse)
async def callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info_raw = await oauth.google.parse_id_token(request, token)

        user_info = {
            "id": user_info_raw["sub"],
            "email": user_info_raw["email"],
            "name": user_info_raw["name"],

        }

        return google_auth_service.handle_google_login(user_info, db)
    except Exception as e:
        return JSONResponse(content={"message":"Login with google failed", "error": str(e)}, status_code=500)
