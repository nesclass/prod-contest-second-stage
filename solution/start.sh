#!/bin/sh
python3 -m alembic upgrade head
python3 -m uvicorn apP:app --host=0.0.0.0 --port=$SERVER_PORT