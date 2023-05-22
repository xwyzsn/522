from fastapi import APIRouter, Depends, HTTPException, status,Form
from pydantic import BaseModel
from models.all_model import Reservation,engine
from datetime import datetime

from typing import Optional,Union

from sqlalchemy.orm import sessionmaker

class ReservationModel(BaseModel):
    rid:Union[int,None] = None
    uid:Union[int,None] = None
    username:Optional[str] = None
    tel:Optional[str] = None
    start_datetime:Optional[datetime] = None
    end_datetime:Optional[datetime] = None
    room_id:Optional[int] = None
    room_name:Optional[str] = None
    status:Optional[str] = None

class ReservationModelStr(BaseModel):
    rid:Union[int,None] = None
    uid:Union[int,None] = None
    username:Optional[str] = None
    tel:Optional[str] = None
    start_datetime:Optional[str] = None
    end_datetime:Optional[str] = None
    room_id:Optional[int] = None
    room_name:Optional[str] = None
    status:Optional[str] = None

def convert_str_to_datetime(s:str):
    return datetime.strptime(s,"%Y-%m-%d %H:%M:%S")

def depend_reservation(reservation:ReservationModelStr):
    if reservation.start_datetime is not None:
        reservation.start_datetime = convert_str_to_datetime(reservation.start_datetime)
    if reservation.end_datetime is not None:
        reservation.end_datetime = convert_str_to_datetime(reservation.end_datetime)
    return reservation


def get_session():
    try:
        session = sessionmaker(bind=engine)()
        yield session
    finally:
        session.close()

router = APIRouter(prefix="/reservation", tags=["reservation"])

@router.post("/add")
def add_reservation(reservation:ReservationModel):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservation = Reservation(**reservation.dict())
        reservation.add_one(session=session)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response

@router.post("/update")
def update_reservation(reservation:ReservationModel= Depends(depend_reservation)):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservationModel = Reservation(**reservation.dict())
        ori_reservation = reservationModel.select_by_id(session=session,id=reservation.rid)
        for k,v in reservation.dict().items():
            if v is not None:
                setattr(ori_reservation,k,v)
        reservationModel.update_one(session=session)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response

@router.delete("/delete/{rid}")
def delete_reservation(rid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservationModel = Reservation()
        reservationModel.delete_by_id(session=session,id=rid)
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response

@router.get("/get/{rid}")
def get_reservation(rid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservationModel = Reservation()
        reservation = reservationModel.select_by_id(session=session,id=rid)
        response["data"] = reservation
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response


@router.get("/get_all")
def get_all_reservation():
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservationModel = Reservation()
        reservations = reservationModel.query_all(session=session)
        response["data"] = reservations
    except Exception as e:
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response


@router.get("/get_by_uid/{uid}")
def get_reservation_by_uid(uid:int):
    response = {"code": 200, "msg": "success","data":None}
    try:
        session = next(get_session())     
        reservationModel = Reservation()
        reservations = reservationModel.select_by_param(session,uid=uid)
        response["data"] = reservations
    except Exception as e:
        print(e)
        response["code"] = 500
        response["msg"] = e
    finally:
        session.close()
    return response


