from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List,Union
from models.all_model import BookMark,engine
from pydantic import BaseModel
from sqlalchemy import Select

def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

class Bookmark_model(BaseModel):
    bid:Union[int,None]
    uid:Union[int,None]
    room_id:Union[int,None]


router = APIRouter(prefix="/bookmark", tags=["bookmark"])

@router.get("/get_bookmark_by_uid/{uid}")
def get_bookmark_by_uid(uid:int):
    response = {"code": 200, "msg": "success","data":None}
    session = next(get_session())
    stmt = session.query(BookMark).filter(BookMark.uid == uid)
    response['data'] = session.scalars(stmt).all()
    return response

@router.post("/add_bookmark")
def add_bookmark(bookmark:Bookmark_model):
    response = {"code": 200, "msg": "success","data":None}
    session = next(get_session())
    session.add(BookMark(**bookmark.dict()))
    session.commit()
    return response

@router.post("/delete_bookmark")
def delete_bookmark(bookmark:Bookmark_model):
    print(bookmark.uid,bookmark.room_id)
    response = {"code": 200, "msg": "success","data":None}
    session = next(get_session())
    stmt = Select(BookMark).where(BookMark.uid == bookmark.uid).where(BookMark.room_id == bookmark.room_id)
    obj = session.scalars(stmt).first()
    session.delete(obj)
    session.commit()
    return response

