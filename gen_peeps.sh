#!/usr/bin/env bash

source venv/bin/activate
while true; do
    python generate_people.py
    sleep 1
done
