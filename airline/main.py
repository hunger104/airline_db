# REST API для управления авиакомпанией (FastAPI)

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
import models
import crud
from db import get_session

app = FastAPI(title="Airline API")

# АЭРОПОРТЫ (Локации вылета и прилета)
@app.get("/airports", response_model=list[models.Airport])
def read_airports(session: Session = Depends(get_session)):
    return crud.get_airports(session)

# САМОЛЕТЫ (Борты)
@app.get("/aircrafts", response_model=list[models.Aircraft])
def read_aircrafts(session: Session = Depends(get_session)):
    return crud.get_aircrafts(session)

# ЭКИПАЖ (Сотрудники)
@app.get("/crew", response_model=list[models.CrewMember])
def read_crew(session: Session = Depends(get_session)):
    return crud.get_crew_members(session)

# ТАРИФЫ (Виды билетов)
@app.get("/tariffs", response_model=list[models.Tariff])
def read_tariffs(session: Session = Depends(get_session)):
    return crud.get_tariffs(session)

# РЕЙСЫ
@app.get("/flights", response_model=list[models.Flight])
def read_flights(session: Session = Depends(get_session)):
    return crud.get_flights(session)

# ПАССАЖИРЫ
@app.get("/passengers", response_model=list[models.Passenger])
def read_passengers(session: Session = Depends(get_session)):
    return crud.get_passengers(session)

# БИЛЕТЫ
@app.get("/tickets", response_model=list[models.Ticket])
def read_tickets(session: Session = Depends(get_session)):
    return crud.get_tickets(session)
