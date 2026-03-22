# Тестирование выборок данных (Запросы к БД Авиакомпании)

from sqlmodel import Session
from db import engine
import crud
import models

def run_tests():
    with Session(engine) as session:
        print("=== 1. Группировка экипажа по должностям ===")
        crew_by_role = crud.crew_grouped_by_role(session)
        for role, members in crew_by_role.items():
            print(f"Должность: {role}")
            for m in members:
                print(f" - {m.full_name} (Налет: {m.flight_hours} ч.)")

        print("\n=== 2. Список всех аэропортов ===")
        airports = crud.list_airports(session)
        for a in airports:
            print(f"[{a.iata_code}] {a.name} — {a.city}, {a.country}")

        print("\n=== 3. Рейсы из первого аэропорта в списке ===")
        if airports:
            first_airport_id = airports[0].id
            flights = crud.flights_by_origin(session, first_airport_id)
            print(f"Вылеты из {airports[0].name}:")
            for f in flights:
                print(f" - Рейс {f.flight_number}, Дата: {f.departure_date}")
        else:
            print("Аэропорты не найдены.")

        print("\n=== 4. Детальная информация по билетам ===")
        detailed_tickets = crud.tickets_with_details(session)
        for t in detailed_tickets:
            print(f"Билет №{t['ticket_number']}: Пассажир {t['passenger_name']}, "
                  f"Рейс {t['flight_number']}, Место {t['seat']}")

        print("\n=== 5. Проверка API-функций (все самолеты) ===")
        aircrafts = crud.get_aircrafts(session)
        for ac in aircrafts:
            print(f"Борт {ac.tail_number}: {ac.model} (Вместимость: {ac.capacity})")

if __name__ == "__main__":
    run_tests()
