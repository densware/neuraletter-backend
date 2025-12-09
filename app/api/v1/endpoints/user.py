from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from app.core.auth import get_current_user
from app.db.session import get_db
from app.services import user_service

router = APIRouter()

class UpdatedUserInfo(BaseModel):
    first_name: str
    last_name: str

@router.get("/me")
def read_current_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return user_service.get_user_by_id(current_user["user_id"], db)
    except Exception as e:
        JSONResponse(
            content={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



@router.patch("/me")
def update_current_user(updated_user_info:UpdatedUserInfo, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return user_service.update_user_info(updated_user_info, current_user, db)
    except Exception as e:
        JSONResponse(
            content={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete("/me")
def delete_user_by_id(current_user:dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        return user_service.delete_user_account(current_user, db)
    except Exception as e:
        JSONResponse(
            content={"message": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
