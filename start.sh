#!/bin/bash
uvicorn finance_system.main:app --host 0.0.0.0 --port $PORT