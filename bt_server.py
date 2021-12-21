from fastapi import FastAPI, Body, Depends
from fastapi.middleware.cors import CORSMiddleware

from services.auth.route import router as AuthRoute
from services.user.route import router as UserRoute
from services.upload.route import router as UploadRoute
from services.baocao.route import router as BaocaoRoute

from fastapi.staticfiles import StaticFiles

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
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(UploadRoute,tags=["Upload FIle"],prefix="")

app.include_router(AuthRoute, tags=["Xác Thực"],prefix="")

app.include_router(UserRoute, tags=["Người dùng"], prefix="")

app.include_router(BaocaoRoute, tags=["Báo cáo"], prefix="")

@app.get("/",tags = ["Welcome"])
async def welcome():
    return {"message":"welcome to my app "}


if __name__ == "__main__":
    uvicorn.run("bt_server:app", host="127.0.0.1", port=8081, reload=True)