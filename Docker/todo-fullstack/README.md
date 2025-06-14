# Fullstack Todo App (Flask + React + Postgres)

## How to run

1. Clone this repo.
2. Run `docker-compose up --build`
3. Backend runs on: http://localhost:5051
4. Frontend runs on: http://localhost:3011

## Features

- User registration/login with JWT
- CRUD todos per user
- React frontend with simple UI
- Fully dockerized with PostgreSQL DB

## Notes

- Change JWT secret key in `backend/app.py` for production
- Database data persists in Docker volume `pgdata`
