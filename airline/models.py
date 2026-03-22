# Список таблиц Авиакомпании

from typing import Optional, List
from datetime import date, time
from sqlmodel import SQLModel, Field, Relationship

# Таблица Аэропортов (Локации)
class Airport(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    iata_code: str = Field(unique=True, index=True) # Например, SVO
    name: str
    city: str
    country: str
    terminals_count: int = 1

    # Связи
    departing_flights: List["Flight"] = Relationship(
        back_populates="origin_airport",
        sa_relationship_kwargs={"foreign_keys": "[Flight.origin_airport_id]"}
    )
    arriving_flights: List["Flight"] = Relationship(
        back_populates="destination_airport",
        sa_relationship_kwargs={"foreign_keys": "[Flight.destination_airport_id]"}
    )

# Таблица Бортов (Самолеты)
class Aircraft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tail_number: str = Field(unique=True) # Бортовой номер
    model: str
    production_year: int
    capacity: int
    is_serviceable: bool = True # Статус ТО

    flights: List["Flight"] = Relationship(back_populates="aircraft")

# Таблица Экипажей (Сотрудники)
class CrewMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    role: str # Пилот, бортпроводник и т.д.
    license_id: str
    flight_hours: int = 0

    flights: List["Flight"] = Relationship(back_populates="crew_member")

# Таблица Тарифов (Виды билетов)
class Tariff(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str # Эконом, Бизнес
    price: float
    baggage_allowance: int # Вес багажа
    is_refundable: bool = False

    tickets: List["Ticket"] = Relationship(back_populates="tariff")

# Таблица Пассажиров
class Passenger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    passport_data: str
    contact_info: Optional[str] = None

    tickets: List["Ticket"] = Relationship(back_populates="passenger")

# Таблица Рейсов
class Flight(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    flight_number: str # Например, SU100

    origin_airport_id: int = Field(foreign_key="airport.id")
    destination_airport_id: int = Field(foreign_key="airport.id")
    aircraft_id: int = Field(foreign_key="aircraft.id")
    crew_member_id: int = Field(foreign_key="crewmember.id")

    departure_date: date
    departure_time: time

    # Связи
    origin_airport: Airport = Relationship(
        back_populates="departing_flights",
        sa_relationship_kwargs={"foreign_keys": "[Flight.origin_airport_id]"}
    )
    destination_airport: Airport = Relationship(
        back_populates="arriving_flights",
        sa_relationship_kwargs={"foreign_keys": "[Flight.destination_airport_id]"}
    )
    aircraft: Aircraft = Relationship(back_populates="flights")
    crew_member: CrewMember = Relationship(back_populates="flights")
    tickets: List["Ticket"] = Relationship(back_populates="flight")

# Таблица Билетов
class Ticket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket_number: str

    flight_id: int = Field(foreign_key="flight.id")
    passenger_id: int = Field(foreign_key="passenger.id")
    tariff_id: int = Field(foreign_key="tariff.id")

    seat_number: Optional[str] = None
    status: str = "Booked" # Забронирован, Оплачен и т.д.

    flight: Flight = Relationship(back_populates="tickets")
    passenger: Passenger = Relationship(back_populates="tickets")
    tariff: Tariff = Relationship(back_populates="tickets")
