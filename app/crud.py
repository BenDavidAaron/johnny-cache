from sqlalchemy.orm import Session
from app import models


def get_record(db: Session, key: str) -> models.Record:
    return db.query(models.Record).filter(models.Record.key == key).first()


def put_record(db: Session, key: str, value: bytes) -> models.Record:
    db_record = models.Record(key=key, value=value)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, key: str) -> None:
    db_record = db.query(models.Record).filter(models.Record.key == key).first()
    db.delete(db_record)
    db.commit()


def delete_records(db: Session) -> None:
    db.query(models.Record).delete()
    db.commit()
