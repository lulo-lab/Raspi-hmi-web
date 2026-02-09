#!/bin/bash

pkill -f uvicorn
pkill -f npm

echo "Starte Backend..."
cd backend
uvicorn main:app --reload &

echo "Starte Frontend..."
cd ../frontend
npm run dev &
