from fastapi import APIRouter, Depends, HTTPException, status,Form
from typing import Optional,Union
from sqlalchemy.orm import sessionmaker
from models.all_model import Users,engine
from pydantic import BaseModel
from base64 import b64decode,b64encode
import json

router = APIRouter(prefix="/user", tags=["user"])





class UserModel(BaseModel):
    uid:Union[int,None] = None
    username:Optional[str] = None
    password:Optional[str] = None
    email:Optional[str] = None
    tel:Optional[str] = None
    role:Optional[str] = None

def get_session():
    try:
        session = sessionmaker(bind=engine)()
        yield session
    finally:
        session.close()



@router.post("/add")
def add_user(user:UserModel):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        user = Users(**user.dict())
        user.add_one(session=session)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        session.close()
    return response

@router.post("/update")
def update_user(user:UserModel):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        userModel = Users(**user.dict())
        print(userModel)
        ori_user = userModel.select_by_id(session=session,id=user.uid)
        for k,v in user.dict().items():
            setattr(ori_user,k,v)
        userModel.update_one(session=session)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        session.close()
    response["data"] = user.dict()
    return response

@router.delete("/delete")
def delete_user(user:UserModel):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        userModel = Users(**user.dict())
        userModel.delete_by_id(session=session,id=user.uid)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        session.close()
    return response

@router.get("/fetchall")
def fetch_all():
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        userModel = Users()
        res = userModel.query_all(session=session)
        response["data"] = res
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        session.close()
    return response


@router.post("/login")
def login(username:str=Form(...),password:str=Form(...)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        userModel = Users()
        res = userModel.select_by_param(sesstion=session,username=username,password=password)
        if res:
            response["data"] = res[0]
            token = {'uid':res[0].uid,'username':res[0].username,'role':res[0].role,'password':res[0].password}
            response["token"] = b64encode(json.dumps(token).encode('utf-8')).decode('utf-8')
        else:
            response["code"] = 500
            response["msg"] = "用户名或密码错误"
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response


@router.get("/get/{uid}")
def get_user(uid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        userModel = Users()
        res = userModel.select_by_id(session=session,id=uid)
        response["data"] = res
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        session.close()
    return response