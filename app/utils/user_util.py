from app.models.user import User


def create_user_response(user: User) -> dict:
    user_response = user.__dict__.copy()
    user_response.pop("hashed_password", None)
    user_response.pop("_sa_instance_state", None)
    user_response.pop("created_at", None)
    user_response.pop("updated_at", None)
    user_response.pop("id", None)
    user_response.pop("is_active", None)

    return user_response