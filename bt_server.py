from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware

from services.auth.route import router as AuthRoute
from services.user.route import router as UserRoute

import uvicorn


app = FastAPI(
    title="API"
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRoute, tags=["Xác Thực"],prefix="")

app.include_router(UserRoute, tags=["Người dùng"], prefix="")

# app.include_router

@app.get("/",tags = ["Welcome"])
async def welcome():
    return {"message":"welcome to my app "}


if __name__ == "__main__":
    uvicorn.run("bt_server:app", host="0.0.0.0", port=8081, reload=True)