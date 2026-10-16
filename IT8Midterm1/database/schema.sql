create schema harborwing_air;
use harborwing_air;


-- 1. stores airport details
create table airport (
    airport_code varchar(10) primary key,
    name varchar(100) not null,
    location varchar(100) not null,
    other_details text
);


-- 2. stores traveler information
create table passenger (
    passenger_id int auto_increment primary key,
    first_name varchar(50) not null,
    second_name varchar(50),
    last_name varchar(50) not null,
    phone_number varchar(20),
    email_address varchar(100),
    address_line varchar(255),
    city varchar(50),
    state_province varchar(50),
    country varchar(50),
    other_details text
);


-- 3. stores optional agent data
create table booking_agent (
    agent_id int auto_increment primary key,
    name varchar(100) not null,
    additional_details text
);


-- 4. required for cost validity rules
create table calendar_date (
    date date primary key,
    day_of_month int not null,
    business_day_indicator boolean not null
);


-- 5. defines scheduled routes
create table flight_schedule (
    flight_number varchar(20) primary key,
    airline_code varchar(10) not null,
    usual_aircraft_type_code varchar(10) not null,
    origin_airport varchar(10) not null,
    destination_airport varchar(10) not null,
    scheduled_departure datetime not null,
    scheduled_arrival datetime not null,
    foreign key (origin_airport) references airport(airport_code),
    foreign key (destination_airport) references airport(airport_code)
);


-- 6. tracks specific operated flight instances
create table flight_leg (
    leg_id int auto_increment primary key,
    flight_number varchar(20) not null,
    origin_airport varchar(10) not null,
    destination_airport varchar(10) not null,
    actual_departure datetime,
    actual_arrival datetime,
    foreign key (flight_number) references flight_schedule(flight_number),
    foreign key (origin_airport) references airport(airport_code),
    foreign key (destination_airport) references airport(airport_code)
);


-- 7. uses composite primary key
create table flight_cost (
    flight_number varchar(20) not null,
    aircraft_type_code varchar(10) not null,
    valid_from date not null,
    valid_to date not null,
    cost_amount decimal(10,2) not null check (cost_amount >= 0),
    primary key (flight_number, aircraft_type_code, valid_from),
    foreign key (flight_number) references flight_schedule(flight_number),
    foreign key (valid_from) references calendar_date(date),
    foreign key (valid_to) references calendar_date(date)
);


-- 8. connects main passenger and optional agent
create table reservation (
    reservation_id int auto_increment primary key,
    main_passenger_id int not null,
    agent_id int,
    reservation_status_code varchar(20) not null,
    ticket_type_code varchar(20) not null,
    travel_class_code varchar(20) not null,
    creation_timestamp datetime not null,
    number_in_party int check (number_in_party > 0),
    foreign key (main_passenger_id) references passenger(passenger_id),
    foreign key (agent_id) references booking_agent(agent_id)
);


-- 9. stores financial transactions
create table payment (
    payment_id int auto_increment primary key,
    payment_status_code varchar(20) not null,
    payment_date datetime not null,
    payment_amount decimal(10,2) check (payment_amount > 0)
);


-- 10. linking table: reservation & payment (many-to-many)
create table reservation_payment_link (
    reservation_id int not null,
    payment_id int not null,
    primary key (reservation_id, payment_id),
    foreign key (reservation_id) references reservation(reservation_id),
    foreign key (payment_id) references payment(payment_id)
);



-- 11. linking table: reservation & flight leg (many-to-many)
create table reservation_leg_link (
    reservation_id int not null,
    leg_id int not null,
    primary key (reservation_id, leg_id),
    foreign key (reservation_id) references reservation(reservation_id),
    foreign key (leg_id) references flight_leg(leg_id)
);