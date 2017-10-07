#!/bin/bash

echo Starting Gunicorn.
exec gunicorn proj1.wsgi:application --bind 0.0.0.0:8000 --workers 3
