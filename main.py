#main.py
from typing import Union

from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from api_router import user_controller,revervation_controller,room_controller,comments_controller,bookmark_controller
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

import json 
from base64 import b64decode,b64encode

app = FastAPI()

app.mount("/img", StaticFiles(directory="anaya/img"), name="static")
app.include_router(user_controller.router)
app.include_router(revervation_controller.router)
app.include_router(room_controller.router)
app.include_router(comments_controller.router)
app.include_router(bookmark_controller.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],


)


STATIC_PATH = {
   "login":"./anaya/home/login.html",
    "home":"./anaya/home/homePage.html",
    "architecture":"./anaya/home/architecture.html",
    "template":"./anaya/archi_class/church.html",
    "church":"./anaya/archi_class/church.html",
    "backend":"./anaya/home/admin.html",

}
WHITE_LIST = [
    "/anaya/login",
    "/anaya/home",
    "/anaya/architecture",
    "/anaya/church",
    "/anaya/img/*",
    "/user/login"
]

@app.middleware("http")
async def pre_check_user(request:Request, call_next):
    # token = request.headers.get("token")
    # path = request.url.path
    # print(path)
    # if path in WHITE_LIST:
        # response = await call_next(request)
        # return respon/se
    # try:
        # decode_str = b64decode(token).decode('utf-8')
        # token = json.loads(decode_str)
    # except:
        # return JSONResponse({"code":500,"msg":"token解析失败"})
    # 打印request中的的数据

    
    response = await call_next(request)
    return response

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/anaya/template/{rid}",response_class=HTMLResponse)
async def get_template(rid:int):
    print("======render template=======")
    path = STATIC_PATH.get("template")
    return open(path).read()
@app.get("/anaya/{file}",response_class=HTMLResponse)
async def get_anaya(file:str):
    if STATIC_PATH.get(file):
        return open(STATIC_PATH.get(file)).read()
    
@app.get("/backend")
async def get_backend(token:str,response_class=RedirectResponse):
    token_str = token
    decode_str = b64decode(token).decode('utf-8')
    token = json.loads(decode_str)
    response =  RedirectResponse(url="http://127.0.0.1:5173/")
    for k,v in token.items():
        response.delete_cookie(k)
    response.set_cookie(key="token",value=token_str)
    token['refresh'] = '0'
    for k,v in token.items():
        response.set_cookie(key=k,value=str(v))
    print(token)
    response.set_cookie(key='test',value='test')
    return response