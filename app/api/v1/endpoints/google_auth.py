from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from app.core.google_oauth import oauth
from app.db.session import get_db
from app.services.auth_service import handle_google_login

router = APIRouter(prefix="/auth/google", tags=["Google Auth"])


@router.get("/login")
async def google_login(request: Request):
    redirect_uri = "http://127.0.0.1:8000/api/v1/auth/google/callback"
    print("REDIRECT URI SENT TO GOOGLE:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="google_callback")
async def google_callback(
    request: Request,
    db: Session = Depends(get_db)
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        return {"message": "Failed to fetch user info"}

    return handle_google_login(user_info, db)
