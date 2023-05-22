from fastapi import APIRouter,Depends
from models.all_model import Comment,engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional,Union
from datetime import datetime

class CommentModel(BaseModel):
    cid:Union[int,None] = None
    uid:Union[int,None] = None
    username:Union[str,None] = None
    comment_time:Union[datetime,None,str] = None
    room_id: Union[int,None] = None
    comment:Union[str,None] = None

def get_session():
    try:
        session = sessionmaker(bind=engine)()
        yield session
    finally:
        session.close()

router = APIRouter(prefix="/comment", tags=["comment"])

def str_to_datetime(s:str):
    return datetime.strptime(s,"%Y-%m-%d %H:%M:%S")


def datetime_inject(comment:CommentModel):
    if type (comment.comment_time) == str:
        comment.comment_time = str_to_datetime(comment.comment_time)
    return comment

@router.post("/add")
def add_comment(comment:CommentModel=Depends(datetime_inject)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comment = Comment(**comment.dict())
        session.add(comment)
        session.commit()
        response["data"] = comment
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response

@router.get("/get/{cid}")
def get_comment(cid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comment = Comment().select_by_id(session=session,id=cid)
        response["data"] = comment
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response

@router.get("/get_all")
def get_all_comment():
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comments = Comment().query_all(session=session)
        response["data"] = comments
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response

@router.post("/update")
def update_comment(comment:CommentModel=Depends(datetime_inject)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comment_modal = Comment(**comment.dict())
        single_comment = Comment().select_by_id(session=session,id=comment_modal.cid)
        for key,value in comment.dict().items():
            setattr(single_comment,key,value)
        session.commit()
        response["data"] = single_comment
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response
    
@router.delete("/delete/{cid}")
def delete_comment(cid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comment = Comment().select_by_id(session=session,id=cid)
        session.delete(comment)
        session.commit()
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response

@router.get("/get_by_room/{rid}")
def get_comment_by_room(rid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())
        comments = Comment().select_by_param(session,room_id=rid)
        response["data"] = comments
    except Exception as e:
        response["code"] = 500
        response["msg"] = str(e)
    finally:
        return response
