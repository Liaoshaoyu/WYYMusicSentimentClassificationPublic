from fastapi import FastAPI, Depends

from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from fastapi.middleware.cors import CORSMiddleware
from routes.admin import router as AdminRouter
from routes.student import router as StudentRouter
from routes.wang_yi_yun import router as WangYiYunRouter

app = FastAPI()

token_listener = JWTBearer()

origins = [
    "http://localhost",
    "http://localhost:8002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app, please see 'http://127.0.0.1:8001/docs'"}


# app.include_router(AdminRouter, tags=["Administrator"], prefix="/admin")
# app.include_router(StudentRouter, tags=["Students"], prefix="/student", dependencies=[Depends(token_listener)])
# app.include_router(StudentRouter, tags=["Students"], prefix="/student")
app.include_router(WangYiYunRouter, tags=["WangYiYun"], prefix="/wyy")
