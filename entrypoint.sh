#!/usr/bin/env bash

export PATH=`poetry env info --path`/bin:$PATH

uvicorn app.main:app --host 0.0.0.0 --port 8000