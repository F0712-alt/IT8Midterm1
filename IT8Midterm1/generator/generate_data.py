import random
from datetime import datetime, timedelta
import mysql.connector
from faker import Faker

fake = Faker()
Faker.seed(42)

# 1. Database Connection
db = mysql.connector.connect(
    host="localhost", user="root", password="admin", database="harborwing_air"
)
cursor = db.cursor()
print("Connected! Generating 50+ rows per table...")

# 2. Independent Parent Tables (50 rows each)
airport_codes, passenger_ids, agent_ids, calendar_dates = [], [], [], []

for _ in range(50):
  # Airport
  code = fake.unique.lexify("???").upper()
  airport_codes.append(code)
  cursor.execute(
      "insert ignore into airport values (%s, %s, %s, %s)",
      (code, fake.city() + " Airport", fake.country(), "Terminal A"),
  )

  # Passenger
  cursor.execute(
      "insert into passenger (first_name, last_name, phone_number, email_address,"
      " city, country) values (%s, %s, %s, %s, %s, %s)",
      (
          fake.first_name(),
          fake.last_name(),
          fake.phone_number(),
          fake.email(),
          fake.city(),
          fake.country(),
      ),
  )
  passenger_ids.append(cursor.lastrowid)

  # Booking Agent
  cursor.execute(
      "insert into booking_agent (name, additional_details) values (%s, %s)",
      (fake.company() + " Travels", "Partner"),
  )
  agent_ids.append(cursor.lastrowid)

# Calendar Dates (60 days)
for i in range(60):
  d = datetime.now().date() + timedelta(days=i)
  calendar_dates.append(d)
  cursor.execute(
      "insert ignore into calendar_date values (%s, %s, %s)",
      (d, d.day, 1 if d.weekday() < 5 else 0),
  )

# 3. Dependent Tables (50 rows each)
flight_numbers, payment_ids, leg_ids, reservation_ids = [], [], [], []

for i in range(50):
  # Flight Schedule
  f_num = f"HW{100+i}"
  flight_numbers.append(f_num)
  orig, dest = random.sample(airport_codes, 2)
  cursor.execute(
      "insert ignore into flight_schedule values (%s, %s, %s, %s, %s, %s, %s)",
      (
          f_num,
          "HW",
          "A320",
          orig,
          dest,
          datetime.now(),
          datetime.now() + timedelta(hours=3),
      ),
  )

  # Payment
  cursor.execute(
      "insert into payment (payment_status_code, payment_date,"
      " payment_amount) values (%s, %s, %s)",
      ("PAID", datetime.now(), round(random.uniform(100, 500), 2)),
  )
  payment_ids.append(cursor.lastrowid)

  # Flight Leg
  cursor.execute(
      "insert into flight_leg (flight_number, origin_airport,"
      " destination_airport, actual_departure, actual_arrival) values (%s, %s,"
      " %s, %s, %s)",
      (f_num, orig, dest, datetime.now(), datetime.now() + timedelta(hours=3)),
  )
  leg_ids.append(cursor.lastrowid)

  # Flight Cost (Composite Key)
  cursor.execute(
      "insert ignore into flight_cost values (%s, %s, %s, %s, %s)",
      (f_num, "A320", calendar_dates[0], calendar_dates[30], 250.00),
  )

  # Reservation
  cursor.execute(
      "insert into reservation (main_passenger_id, agent_id,"
      " reservation_status_code, ticket_type_code, travel_class_code,"
      " creation_timestamp, number_in_party) values (%s, %s, %s, %s, %s, %s,"
      " %s)",
      (
          random.choice(passenger_ids),
          random.choice(agent_ids),
          "CONFIRMED",
          "E-TICKET",
          "ECONOMY",
          datetime.now(),
          2,
      ),
  )
  reservation_ids.append(cursor.lastrowid)

# 4. Linking Tables (Many-to-Many with 50+ unique rows)
linked_payments = set()
while len(linked_payments) < 50:
  linked_payments.add(
      (random.choice(reservation_ids), random.choice(payment_ids))
  )

for res_id, pay_id in linked_payments:
  cursor.execute(
      "insert ignore into reservation_payment_link values (%s, %s)",
      (res_id, pay_id),
  )

linked_legs = set()
while len(linked_legs) < 50:
  linked_legs.add((random.choice(reservation_ids), random.choice(leg_ids)))

for res_id, l_id in linked_legs:
  cursor.execute(
      "insert ignore into reservation_leg_link values (%s, %s)", (res_id, l_id)
  )

db.commit()

# 5. Verification Count
print("\n--- ROW COUNT VERIFICATION ---")
for t in [
    "airport",
    "passenger",
    "booking_agent",
    "calendar_date",
    "flight_schedule",
    "flight_leg",
    "flight_cost",
    "reservation",
    "payment",
    "reservation_payment_link",
    "reservation_leg_link",
]:
  cursor.execute(f"select count(*) from {t}")
  print(f"{t}: {cursor.fetchone()[0]} rows")

cursor.close()
db.close()