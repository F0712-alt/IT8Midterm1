# HarborWing Air - Midterm Database Project

## Overview
This project implements a relational database management system for **HarborWing Air** using MySQL and Python. The database schema consists of 11 core tables designed to handle airports, passengers, booking agents, flight schedules, flight legs, pricing, reservations, payments, and many-to-many relationship linking tables.

---

## Repository Structure
```text
IT8Midterm1/
│
├── database/
│   ├── schema.sql              # Clean SQL script to create the schema and tables
│   ├── harborwing_air.mwb      # MySQL Workbench EER diagram project file
│   └── eer_diagram.png         # Exported image of the EER diagram
│
├── generator/
│   ├── generate_data.py        # Python script utilizing Faker to populate 50+ rows per table
│   └── requirements.txt        # Project dependencies (faker, mysql-connector-python)
│
└── README.md                   # Project documentation, design notes, and required queries