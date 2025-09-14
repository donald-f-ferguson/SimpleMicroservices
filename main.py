from __future__ import annotations

import os
import socket
import logging
from datetime import datetime
from uuid import UUID, uuid4
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.middleware.cors import CORSMiddleware

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.empoyee import EmployeeCreate, EmployeeRead, EmployeeUpdate
from models.paycheck import PaycheckCreate, PaycheckRead, PaycheckUpdate

port = int(os.environ.get("FASTAPIPORT", 8001))

# ---------------------------------------------------------------------
# Logging (simple)
# ---------------------------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("person-address-api")

# ---------------------------------------------------------------------
# Fake in-memory "databases" (UUID keys)
# ---------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
employees: Dict[UUID, EmployeeRead] = {}
paychecks: Dict[UUID, PaycheckRead] = {}

# ---------------------------------------------------------------------
# App + production-minded settings (CORS, metadata)
# ---------------------------------------------------------------------
app = FastAPI(
    title="Person/Address/Employee/Paycheck API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Employee and Paycheck",
    version="0.1.0",
)

# Allow origins as needed in production - tighten for real deployments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <--- restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    # safe ip lookup
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "unknown"
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=ip,
        echo=echo,
        path_echo=path_echo,
    )


# ---------------------------------------------------------------------
# Health endpoints
# ---------------------------------------------------------------------
@app.get("/health", response_model=Health, tags=["health"])
def get_health_no_path(
    echo: Optional[str] = Query(None, description="Optional echo string")
):
    return make_health(echo=echo, path_echo=None)


@app.get("/health/{path_echo}", response_model=Health, tags=["health"])
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: Optional[str] = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# ---------------------------------------------------------------------
# Address endpoints
# ---------------------------------------------------------------------
@app.post(
    "/addresses",
    response_model=AddressRead,
    status_code=status.HTTP_201_CREATED,
    tags=["addresses"],
)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(
            status_code=400, detail="Address with this ID already exists"
        )
    addr_read = AddressRead(**address.model_dump())
    addresses[addr_read.id] = addr_read
    logger.info("Created address %s", addr_read.id)
    return addr_read


@app.get("/addresses", response_model=List[AddressRead], tags=["addresses"])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())
    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]
    return results


@app.get("/addresses/{address_id}", response_model=AddressRead, tags=["addresses"])
def get_address(address_id: UUID = Path(...)):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]


@app.patch("/addresses/{address_id}", response_model=AddressRead, tags=["addresses"])
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    logger.info("Updated address %s", address_id)
    return addresses[address_id]


# ---------------------------------------------------------------------
# Person endpoints
# ---------------------------------------------------------------------
@app.post(
    "/persons",
    response_model=PersonRead,
    status_code=status.HTTP_201_CREATED,
    tags=["persons"],
)
def create_person(person: PersonCreate):
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    logger.info("Created person %s", person_read.id)
    return person_read


@app.get("/persons", response_model=List[PersonRead], tags=["persons"])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(
        None, description="Filter by date of birth (YYYY-MM-DD)"
    ),
    city: Optional[str] = Query(
        None, description="Filter by city of at least one address"
    ),
    country: Optional[str] = Query(
        None, description="Filter by country of at least one address"
    ),
):
    results = list(persons.values())
    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [
            p for p in results if any(addr.country == country for addr in p.addresses)
        ]
    return results


@app.get("/persons/{person_id}", response_model=PersonRead, tags=["persons"])
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]


@app.patch("/persons/{person_id}", response_model=PersonRead, tags=["persons"])
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    logger.info("Updated person %s", person_id)
    return persons[person_id]


# ---------------------------------------------------------------------
# Employee endpoints (CRUD)
# ---------------------------------------------------------------------
@app.get("/employees", response_model=List[EmployeeRead], tags=["employees"])
def list_employees():
    return list(employees.values())


@app.post(
    "/employees",
    response_model=EmployeeRead,
    status_code=status.HTTP_201_CREATED,
    tags=["employees"],
)
def create_employee(payload: EmployeeCreate):
    new_id = uuid4()
    emp = EmployeeRead(id=new_id, **payload.model_dump())
    employees[new_id] = emp
    logger.info("Created employee %s", new_id)
    return emp


@app.get("/employees/{employee_id}", response_model=EmployeeRead, tags=["employees"])
def get_employee(employee_id: UUID):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees[employee_id]


@app.put("/employees/{employee_id}", response_model=EmployeeRead, tags=["employees"])
def update_employee(employee_id: UUID, payload: EmployeeUpdate):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    stored = employees[employee_id].model_dump()
    stored.update(payload.model_dump(exclude_unset=True))
    employees[employee_id] = EmployeeRead(**stored)
    logger.info("Updated employee %s", employee_id)
    return employees[employee_id]


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["employees"],
)
def delete_employee(employee_id: UUID):
    if employee_id not in employees:
        raise HTTPException(status_code=404, detail="Employee not found")
    del employees[employee_id]
    logger.info("Deleted employee %s", employee_id)
    return None


# ---------------------------------------------------------------------
# Paycheck endpoints (CRUD)
# ---------------------------------------------------------------------
@app.get("/paychecks", response_model=List[PaycheckRead], tags=["paychecks"])
def list_paychecks():
    return list(paychecks.values())


@app.post(
    "/paychecks",
    response_model=PaycheckRead,
    status_code=status.HTTP_201_CREATED,
    tags=["paychecks"],
)
def create_paycheck(payload: PaycheckCreate):
    # optional: validate employee exists
    if payload.employee_id not in employees:
        raise HTTPException(status_code=400, detail="employee_id does not exist")
    new_id = uuid4()
    pc = PaycheckRead(id=new_id, **payload.model_dump())
    paychecks[new_id] = pc
    logger.info("Created paycheck %s", new_id)
    return pc


@app.get("/paychecks/{paycheck_id}", response_model=PaycheckRead, tags=["paychecks"])
def get_paycheck(paycheck_id: UUID):
    if paycheck_id not in paychecks:
        raise HTTPException(status_code=404, detail="Paycheck not found")
    return paychecks[paycheck_id]


@app.put("/paychecks/{paycheck_id}", response_model=PaycheckRead, tags=["paychecks"])
def update_paycheck(paycheck_id: UUID, payload: PaycheckUpdate):
    if paycheck_id not in paychecks:
        raise HTTPException(status_code=404, detail="Paycheck not found")
    stored = paychecks[paycheck_id].model_dump()
    stored.update(payload.model_dump(exclude_unset=True))
    paychecks[paycheck_id] = PaycheckRead(**stored)
    logger.info("Updated paycheck %s", paycheck_id)
    return paychecks[paycheck_id]


@app.delete(
    "/paychecks/{paycheck_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["paychecks"],
)
def delete_paycheck(paycheck_id: UUID):
    if paycheck_id not in paychecks:
        raise HTTPException(status_code=404, detail="Paycheck not found")
    del paychecks[paycheck_id]
    logger.info("Deleted paycheck %s", paycheck_id)
    return None


# ---------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------
@app.get("/", tags=["root"])
def root():
    return {
        "message": "Welcome to the Person/Address/Employee/Paycheck API. See /docs for OpenAPI UI."
    }


# ---------------------------------------------------------------------
# Entrypoint for `python main.py`
# (for production run with gunicorn/uvicorn recommended)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    # In production you will likely run via: uvicorn main:app --host 0.0.0.0 --port 8001
    # or with gunicorn + uvicorn workers
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
