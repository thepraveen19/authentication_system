from fastapi import FastAPI
from fastapi import FastAPI
from routes.login import router as login_router
from routes.register import router as register_router
from routes.reset_password import router as reset_password_router

app = FastAPI()

# Include routers
app.include_router(login_router)
app.include_router(register_router)
app.include_router(reset_password_router)

