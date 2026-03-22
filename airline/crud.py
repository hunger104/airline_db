# Функции для выборки данных Авиакомпании

from sqlmodel import Session, select
import models
from typing import List, Dict

# Группировка экипажа по должностям (аналог сотрудников по локациям)
def crew_grouped_by_role(session: Session) -> Dict[str, List[models.CrewMember]]:
    stmt = select(models.CrewMember).order_by(models.CrewMember.id)
    crew = session.exec(stmt).all()
    result = {}
    for c in crew:
        role = c.role
        result.setdefault(role, []).append(c)
    return result

# Список всех аэропортов
def list_airports(session: Session) -> List[models.Airport]:
    statement = select(models.Airport).order_by(models.Airport.id)
    return session.exec(statement).all()

# Рейсы, вылетающие из конкретного аэропорта
def flights_by_origin(session: Session, airport_id: int) -> List[models.Flight]:
    statement = select(models.Flight).where(models.Flight.origin_airport_id == airport_id).order_by(models.Flight.id)
    return session.exec(statement).all()

# Список билетов с информацией о рейсе и пассажире (детальный список)
def tickets_with_details(session: Session) -> List[Dict]:
    statement = select(models.Ticket)
    tickets = session.exec(statement).all()
    out = []
    for t in tickets:
        f = t.flight
        p = t.passenger
        out.append({
            "ticket_id": t.id,
            "ticket_number": t.ticket_number,
            "flight_number": f.flight_number if f else None,
            "passenger_name": p.full_name if p else None,
            "seat": t.seat_number
        })
    return out

# === Функции для FastAPI (используются в main.py) === #

def get_airports(session: Session):
    return session.exec(select(models.Airport)).all()

def get_aircrafts(session: Session):
    return session.exec(select(models.Aircraft)).all()

def get_crew_members(session: Session):
    return session.exec(select(models.CrewMember)).all()

def get_tariffs(session: Session):
    return session.exec(select(models.Tariff)).all()

def get_flights(session: Session):
    return session.exec(select(models.Flight)).all()

def get_passengers(session: Session):
    return session.exec(select(models.Passenger)).all()

def get_tickets(session: Session):
    return session.exec(select(models.Ticket)).all()
