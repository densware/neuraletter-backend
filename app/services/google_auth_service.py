from platform import system

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.core.auth import create_jwt_token
from app.db.session import get_db
from app.models.user import User


def handle_google_login(user_info: dict, db: Session ) -> JSONResponse:

    try:
        user = db.query(User).filter(User.email == user_info["email"]).first()
        if not user:
            # Create new user
            user = User(
                id=user_info["id"],
                email=user_info["email"],
                first_name=user_info.get("name", ""),
                is_verified=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        token = create_jwt_token(user.id, user.email)
        return JSONResponse(content={"message":"Login successful", "access_token": token, "token_type": "bearer"}, status_code=200)
    except Exception as e:
        db.rollback()
        print(e)
        return JSONResponse(content={"message":"Login with google failed", "error": str(e)}, status_code=401)


