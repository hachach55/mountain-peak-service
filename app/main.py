from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from typing import List

from . import models, schemas
from .database import engine, get_db

import os
from dotenv import load_dotenv

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mountain Peak Service",
              description="an API for storing and retrieving mountain peaks information",
              version="1.0.0",
              openapi_tags=[{
                  "name": "peaks",
                  "description": "Operations with mountain peaks"
              }])

load_dotenv()
# SECRET_KEY = os.getenv("SECRET_KEY")

@app.get('/', response_class=HTMLResponse)
async def root():
        html_content = f"""
    <html>
        <head>
            <title>Mountain Peak API</title>
        </head>
        <body>
            <h1>Welcome to the Mountain Peak API</h1>
            <p>This API provides information about mountain peaks.</p>
            <p>To access the API documentation, please visit:</p>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
            </ul>
        </body>
    </html>
    """
        return HTMLResponse(content=html_content, status_code=200)

@app.post("/peaks/", response_model=schemas.Peak)
def create_peak(peak: schemas.PeakCreate, db: Session = Depends(get_db)):
    db_peak = models.Peak(**peak.dict())
    db.add(db_peak)
    db.commit()
    db.refresh(db_peak)
    return db_peak

@app.get("/peaks/", response_model=List[schemas.Peak])
def read_peaks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    peaks = db.query(models.Peak).offset(skip).limit(limit).all()
    return peaks

@app.get("/peaks/{peak_id}", response_model=schemas.Peak)
def read_peak(peak_id: int, db: Session = Depends(get_db)):
    db_peak = db.query(models.Peak).filter(models.Peak.id == peak_id).first()
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    return db_peak

@app.put("/peaks/{peak_id}", response_model=schemas.Peak)
def update_peak(peak_id: int, peak: schemas.PeakCreate, db: Session = Depends(get_db)):
    db_peak = db.query(models.Peak).filter(models.Peak.id == peak_id).first()
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    for var, value in vars(peak).items():
        setattr(db_peak, var, value) if value else None
    db.add(db_peak)
    db.commit()
    db.refresh(db_peak)
    return db_peak

@app.delete("/peaks/{peak_id}", response_model=schemas.Peak)
def delete_peak(peak_id: int, db: Session = Depends(get_db)):
    db_peak = db.query(models.Peak).filter(models.Peak.id == peak_id).first()
    if db_peak is None:
        raise HTTPException(status_code=404, detail="Peak not found")
    db.delete(db_peak)
    db.commit()
    return db_peak

@app.post("/peaks/search/", response_model=List[schemas.Peak])
def search_peaks(bbox: schemas.BoundingBox, db: Session = Depends(get_db)):
    peaks = db.query(models.Peak).filter(
        models.Peak.latitude >= bbox.min_lat,
        models.Peak.latitude <= bbox.max_lat,
        models.Peak.longitude >= bbox.min_lon,
        models.Peak.longitude <= bbox.max_lon
    ).all()
    return peaks