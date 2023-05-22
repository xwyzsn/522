from fastapi import APIRouter, Depends, HTTPException, status,Form,File,UploadFile
from typing import List
import uuid
from pydantic import BaseModel
from models.all_model import Room,engine
from typing import Optional,Union

from sqlalchemy.orm import sessionmaker

class RoomModel(BaseModel):
    rid:Union[int,None] = None
    room_name:Optional[str] = None
    room_type:Optional[str] = None
    room_desc:Optional[str] = None
    room_cover_pic:Optional[str] = None
    room_inner_pic:Optional[str] = None


class RoomModelPre(BaseModel):
    rid:Union[int,None] = None
    room_name:Optional[str] = None
    room_type:Optional[str] = None
    room_desc:Optional[str] = None
    room_cover_pic:Optional[UploadFile] = None
    room_inner_pic:Optional[UploadFile] = None


def generate_file_name(file_name:str):
    ext = file_name.split(".")[-1]
    return str(uuid.uuid4().hex)+"."+ext
def depend_room(rid:Union[int,None]=Form(default=None),room_name:str=Form(),room_type:str=Form(),room_desc:str=Form(),room_cover_pic:  UploadFile=File(None),room_inner_pic:UploadFile=File(None)):
    base_url = "http://127.0.0.1:8000/img/"
    if room_cover_pic is not None:
        print(room_cover_pic)
        room_cover_pic_name = generate_file_name(room_cover_pic.filename)
        with open('./anaya/img/'+room_cover_pic_name,'wb') as f:
            f.write(room_cover_pic.file.read())
        room_cover_pic = base_url+room_cover_pic_name
    if room_inner_pic is not None:
        room_inner_pic_name = generate_file_name(room_inner_pic.filename)
        with open('./anaya/img/'+room_inner_pic_name,'wb') as f:
            f.write(room_inner_pic.file.read())
        room_inner_pic = base_url+room_inner_pic_name
    room = RoomModel(rid=rid,room_name=room_name,room_type=room_type,room_desc=room_desc,room_cover_pic=room_cover_pic,room_inner_pic=room_inner_pic)
    return room

def get_session():
    try:
        session = sessionmaker(bind=engine)()
        yield session
    finally:
        session.close()

router = APIRouter(prefix="/room", tags=["room"])

@router.post("/add")
def add_room(room:RoomModel = Depends(depend_room)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        room = Room(**room.dict())
        room.add_one(session=session)
    except Exception as e:
        print(e)
        response["code"] = 500
        response["msg"] = e
    finally:
        return response

@router.get("/get/{rid}")
def get_room(rid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        room = Room().select_by_id(session=session,id=rid)
        response["data"] = room
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        return response
    
@router.get("/get_all")
def get_all_room():
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        rooms = Room().query_all(session=session)
        response["data"] = rooms
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        return response
    
@router.post("/update")
def update_room(room:RoomModel=Depends(depend_room)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        room_modal = Room(**room.dict())
        single_room = Room().select_by_id(session=session,id=room_modal.rid)
        for key,value in room.dict().items():
            if value is not None:
                setattr(single_room,key,value)
        single_room.update_one(session=session)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        return response
    
@router.delete("/delete/{rid}")
def delete_room(rid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        Room().delete_by_id(session=session,id=rid)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        return response

@router.get("/get_by_roomid_list")
def get_by_roomid_list(rid_list:str):
    rid_list = rid_list.split(",")
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        rooms = session.query(Room).filter(Room.rid.in_(rid_list)).all()
        response["data"] = rooms
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
        print(e)
    finally:
        return response

