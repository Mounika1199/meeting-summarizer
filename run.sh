#!/bin/bash
export PYTHONPATH=$(pwd)
uvicorn app.main:app --host 0.0.0.0 --port 8009 --reload
