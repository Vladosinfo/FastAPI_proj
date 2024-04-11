from typing import List
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    return contacts


@router.get("/search/by_name/{contact_name}", response_model=List[ContactResponse])
async def read_contacts_by_name(contact_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_name(contact_name, db)
    return contacts


@router.get("/search/by_surname/{contact_surname}", response_model=List[ContactResponse])
async def read_contacts_by_surname(contact_surname: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_surname(contact_surname, db)
    return contacts
    

@router.get("/search/by_birthday_data/", response_model=List[ContactResponse])
async def read_contacts_by_nearest_7_days_birthday(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_nearest_7_days_birthday(db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/search/by_email/{contact_email}", response_model=ContactResponse)
async def read_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactResponse, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactResponse, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact
