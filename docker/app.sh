#!/bin/bash

alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class uvicorn.worker.UvicornWorker --bind