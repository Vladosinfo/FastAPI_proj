from typing import List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactResponse
from sqlalchemy import extract

async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contacts_by_name(name: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.name == name).all()


async def get_contacts_by_surname(surname: str, db: Session) -> List[Contact]:
    return db.query(Contact).filter(Contact.surname == surname).all()




async def get_contacts_nearest_7_days_birthday(db: Session) -> List[Contact]:

    # today_for_testing = datetime(year=2024, month=12, day=29)
    # today_for_testing = datetime(year=2024, month=4, day=28)
    # today_for_testing = datetime(year=2024, month=4, day=12)
    # today = today_for_testing.date()
    
    today = datetime.now().date()
    cday7 = today + timedelta(days=7)

    if today.month == 12:

        return db.query(Contact).filter(
            (
                (extract('month', Contact.birthday) >= today.month)
                | ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day))
                | ((extract('month', Contact.birthday) == 1) & (today.month == 12))
            )
            & (
                (extract('month', Contact.birthday) > cday7.month)
                | ((extract('month', Contact.birthday) == cday7.month) & (extract('day', Contact.birthday) <= cday7.day))
                | ((extract('month', Contact.birthday) == 1) & (cday7.month == 1) & (extract('day', Contact.birthday) <= cday7.day))
            )
        ).all()
    
    else:

        return db.query(Contact).filter(
            (
                (extract('month', Contact.birthday) > today.month)
                | ((extract('month', Contact.birthday) == today.month) & (extract('day', Contact.birthday) >= today.day))
            )
            & (
                (extract('month', Contact.birthday) < cday7.month)
                | ((extract('month', Contact.birthday) == cday7.month) & (extract('day', Contact.birthday) <= cday7.day))
            )        
        ).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    res = db.query(Contact).filter(Contact.id == contact_id).first()
    return res


async def get_contact_by_email(email: int, db: Session) -> Contact:
    res = db.query(Contact).filter(Contact.email == email).first()
    return res


async def create_contact(body: ContactResponse, db: Session) -> Contact:
    contact = Contact(name=body.name, surname=body.surname, email=body.email, phone=body.phone, 
                      birthday=body.birthday, additional=body.additional)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact(contact_id: int, body: ContactResponse, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional = body.additional
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact
