# Заполняем таблицы минимальным набором данных (Seed)

from sqlmodel import Session
from db import engine
import models
from datetime import date, time

def seed_data():
    with Session(engine) as session:
        # 1. Добавляем Аэропорты
        svo = models.Airport(iata_code="SVO", name="Шереметьево", city="Москва", country="Россия", terminals_count=5)
        led = models.Airport(iata_code="LED", name="Пулково", city="Санкт-Петербург", country="Россия", terminals_count=2)
        session.add(svo)
        session.add(led)

        # 2. Добавляем Борты (Самолеты)
        boeing = models.Aircraft(tail_number="RA-73001", model="Boeing 737-800", production_year=2018, capacity=189, is_serviceable=True)
        airbus = models.Aircraft(tail_number="RA-32002", model="Airbus A320", production_year=2020, capacity=160, is_serviceable=True)
        session.add(boeing)
        session.add(airbus)

        # 3. Добавляем Экипаж
        pilot = models.CrewMember(full_name="Иванов Иван Иванович", role="Командир", license_id="ATPL-001", flight_hours=5500)
        steward = models.CrewMember(full_name="Петрова Анна Сергеевна", role="Бортпроводник", license_id="CABIN-99", flight_hours=1200)
        session.add(pilot)
        session.add(steward)

        # 4. Добавляем Тарифы
        economy = models.Tariff(name="Эконом", price=5500.0, baggage_allowance=23, is_refundable=False)
        business = models.Tariff(name="Бизнес", price=25000.0, baggage_allowance=40, is_refundable=True)
        session.add(economy)
        session.add(business)

        # 5. Добавляем Пассажира
        passenger = models.Passenger(full_name="Сидоров Алексей Петрович", passport_data="4512 000111", contact_info="alex@mail.ru")
        session.add(passenger)

        # Сначала сохраняем, чтобы получить ID для связей
        session.commit()

        # 6. Добавляем Рейс (используем ID созданных объектов)
        flight = models.Flight(
            flight_number="SU100",
            origin_airport_id=svo.id,
            destination_airport_id=led.id,
            aircraft_id=boeing.id,
            crew_member_id=pilot.id,
            departure_date=date(2023, 12, 25),
            departure_time=time(10, 30)
        )
        session.add(flight)
        session.commit()

        # 7. Добавляем Билет
        ticket = models.Ticket(
            ticket_number="5551234567890",
            flight_id=flight.id,
            passenger_id=passenger.id,
            tariff_id=economy.id,
            seat_number="12A",
            status="Paid"
        )
        session.add(ticket)

        session.commit()
        print("Данные авиакомпании успешно загружены!")

if __name__ == "__main__":
    seed_data()
