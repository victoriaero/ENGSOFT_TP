# app/routers/sample_rows.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict
from itertools import islice
from pathlib import Path
import csv
