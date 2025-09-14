from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.hospital import HospitalCreate, HospitalRead, HospitalUpdate
from models.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
hospitals: Dict[UUID, HospitalRead] = {}
appointments: Dict[UUID, AppointmentRead] = {}

app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Hospital and Appointment",
    version="0.1.0",
)

# ---------------------------------------------------------------------
# Hospital endpoints
# ---------------------------------------------------------------------
@app.post("/hospitals", response_model=HospitalRead, status_code=201, summary="Create a hospital")
def create_hospital(hospital: HospitalCreate):
    """Create a new hospital resource."""
    if hospital.id in hospitals:
        raise HTTPException(status_code=400, detail="Hospital with this ID already exists")
    hospitals[hospital.id] = HospitalRead(**hospital.model_dump())
    return hospitals[hospital.id]

@app.get("/hospitals", response_model=List[HospitalRead], summary="List all hospitals")
def list_hospitals(
    name: Optional[str] = Query(None, description="Filter by hospital name"),
    city: Optional[str] = Query(None, description="Filter by city (in address)"),
    contact: Optional[str] = Query(None, description="Filter by contact"),
):
    """List all hospitals, with optional filters."""
    results = list(hospitals.values())
    if name is not None:
        results = [h for h in results if h.name == name]
    if city is not None:
        results = [h for h in results if city.lower() in (h.address or "").lower()]
    if contact is not None:
        results = [h for h in results if h.contact == contact]
    return results

@app.get("/hospitals/{hospital_id}", response_model=HospitalRead, summary="Get a hospital by ID")
def get_hospital(hospital_id: UUID = Path(..., description="Hospital UUID")):
    """Get a hospital by its UUID."""
    if hospital_id not in hospitals:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospitals[hospital_id]

@app.patch("/hospitals/{hospital_id}", response_model=HospitalRead, summary="Update a hospital")
def update_hospital(
    update: HospitalUpdate, 
    hospital_id: UUID = Path(..., description="Hospital UUID"), ):
    """Update a hospital by its UUID."""
    if hospital_id not in hospitals:
        raise HTTPException(status_code=404, detail="Hospital not found")
    stored = hospitals[hospital_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    hospitals[hospital_id] = HospitalRead(**stored)
    return hospitals[hospital_id]

@app.delete(
    "/hospitals/{hospital_id}",
    status_code=204,
    summary="Delete a hospital",
    description="Delete a hospital by its UUID. Returns 204 if successful, 404 if not found.",
)
def delete_hospital(hospital_id: UUID = Path(..., description="Hospital UUID")):
    """Delete a hospital by its UUID."""
    if hospital_id not in hospitals:
        raise HTTPException(status_code=404, detail="Hospital not found")
    del hospitals[hospital_id]
    return

# ---------------------------------------------------------------------
# Appointment endpoints
# ---------------------------------------------------------------------
@app.post("/appointments", response_model=AppointmentRead, status_code=201, summary="Create an appointment")
def create_appointment(appointment: AppointmentCreate):
    """Create a new appointment resource."""
    if appointment.id in appointments:
        raise HTTPException(status_code=400, detail="Appointment with this ID already exists")
    appointments[appointment.id] = AppointmentRead(**appointment.model_dump())
    return appointments[appointment.id]

@app.get("/appointments", response_model=List[AppointmentRead], summary="List all appointments")
def list_appointments(
    person_id: Optional[str] = Query(None, description="Filter by person UNI"),
    hospital_id: Optional[UUID] = Query(None, description="Filter by hospital ID"),
):
    """List all appointments, with optional filters."""
    results = list(appointments.values())
    if person_id is not None:
        results = [a for a in results if a.person_id == person_id]
    if hospital_id is not None:
        results = [a for a in results if a.hospital_id == hospital_id]
    return results

@app.get("/appointments/{appointment_id}", response_model=AppointmentRead, summary="Get an appointment by ID")
def get_appointment(appointment_id: UUID = Path(..., description="Appointment UUID")):
    """Get an appointment by its UUID."""
    if appointment_id not in appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointments[appointment_id]

@app.patch("/appointments/{appointment_id}", response_model=AppointmentRead, summary="Update an appointment")
def update_appointment(
    update: AppointmentUpdate,
    appointment_id: UUID = Path(..., description="Appointment UUID"),
):
    """Update an appointment by its UUID."""
    if appointment_id not in appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")
    stored = appointments[appointment_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    appointments[appointment_id] = AppointmentRead(**stored)
    return appointments[appointment_id]

@app.delete(
    "/appointments/{appointment_id}",
    status_code=204,
    summary="Delete an appointment",
    description="Delete an appointment by its UUID. Returns 204 if successful, 404 if not found.",
)
def delete_appointment(appointment_id: UUID = Path(..., description="Appointment UUID")):
    """Delete an appointment by its UUID."""
    if appointment_id not in appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")
    del appointments[appointment_id]
    return

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
