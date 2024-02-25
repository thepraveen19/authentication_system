from fastapi import FastAPI
from fastapi import FastAPI
from routes.authentication import router as authentication_router
# from routes.user import router as user_router
# from routes.password_reset import router as password_reset_router

app = FastAPI()

# Include routers
app.include_router(authentication_router)
# app.include_router(user_router)
# app.include_router(password_reset_router)
