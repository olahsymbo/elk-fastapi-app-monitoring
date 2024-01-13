import logging
import os
from uuid import uuid4

from src.elk_fastapi_app_monitoring.database.db import SessionLocal
from src.elk_fastapi_app_monitoring.models.users import User
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

if not os.path.exists("./logs"):
    os.mkdir("./logs")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.StreamHandler()
file_handler = logging.FileHandler("./logs/api_log.log")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

router = APIRouter()


@router.post("/create_user")
async def create_user(request: Request):
    if request.method == "POST":
        try:
            user = User(name=f"User_{uuid4()}", email=f"user_{uuid4()}@example.com")
            db = SessionLocal()
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info([f"User {uuid4()} created successfully"])
            return JSONResponse(
                {
                    "data": {"id": user.id, "name": user.name, "email": user.email},
                    "message": "User created successfully",
                    "errors": None,
                    "status": 200,
                },
                status_code=200,
            )
        except Exception as error:
            logger.error(["process failed", error])
            return JSONResponse(
                {
                    "message": "Failed to create user",
                    "errors": str(error),
                    "status": 400,
                },
                status_code=400,
            )


@router.get("/get_user/{user_id}")
async def get_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if user:
        logger.info([f"User {user_id} fetched"])
        return JSONResponse(
            {
                "data": {"id": user.id, "name": user.name, "email": user.email},
                "message": "User found",
                "errors": None,
                "status": 200,
            },
            status_code=200,
        )
    else:
        logger.error([f"User {user_id} not found"])
        return JSONResponse(
            {
                "message": "User not found",
                "errors": None,
                "status": 404,
            },
            status_code=404,
        )


@router.put("/update_user/{user_id}")
async def update_user(user_id: int, request: Request):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        try:
            data = await request.json()
            user.name = data["name"]
            user.email = data["email"]
            db.commit()
            db.refresh(user)
            logger.error([f"User {user_id} updated successfully"])
            return JSONResponse(
                {
                    "data": {"id": user.id, "name": user.name, "email": user.email},
                    "message": "User updated successfully",
                    "errors": None,
                    "status": 200,
                },
                status_code=200,
            )
        except Exception as error:
            db.rollback()
            logger.error(["process failed", error])
            return JSONResponse(
                {
                    "message": "Failed to update user",
                    "errors": str(error),
                    "status": 400,
                },
                status_code=400,
            )
    else:
        logger.error(["User not found"])
        return JSONResponse(
            {
                "message": "User not found",
                "errors": None,
                "status": 404,
            },
            status_code=404,
        )


@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        db.delete(user)
        db.commit()
        db.close()

        logger.info([f"User {user_id} deleted"])

        return JSONResponse(
            {
                "message": "User deleted successfully",
                "errors": None,
                "status": 200,
            },
            status_code=200,
        )
    else:
        logger.info([f"User {user_id} not found"])
        return JSONResponse(
            {
                "message": "User not found",
                "errors": None,
                "status": 404,
            },
            status_code=404,
        )
