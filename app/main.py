import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.endpoints import auth, health, user_verification, user, google_auth, reset_password
from app.core.config import settings
from app.db.init_db import init_db
from app.api.v1.endpoints.google_auth import router as google_auth_router

app = FastAPI(title="Neuraletter API")

# ✅ CORS MUST BE HERE — ON THE REAL APP
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site="lax",
    https_only=False,
)
# Create database tables if they don't exist
init_db()

print("CORS", settings.CORS_ALLOWED_ORIGINS)

# ✅ Routers AFTER middleware
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(user_verification.router, prefix="/api/v1/user/verification", tags=["User Verification"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(google_auth.router, prefix="/api/v1/auth", tags=["Google Auth"])
app.include_router(reset_password.router, prefix="/api/v1/user", tags=["Reset Password"])
app.include_router(google_auth_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
