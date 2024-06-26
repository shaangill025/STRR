"""
ORM Mapping for Invoices
"""
from __future__ import annotations

from sqlalchemy import Enum
from sqlalchemy.orm import relationship

from strr_api.enums.enum import PaymentStatus

from .db import db


class Invoice(db.Model):
    """Invoice"""

    __tablename__ = "invoices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registration_id = db.Column(db.Integer, db.ForeignKey("registrations.id"), nullable=False)
    invoice_id = db.Column(db.Integer, nullable=False)
    payment_status_code = db.Column(Enum(PaymentStatus), nullable=False)
    payment_completion_date = db.Column(db.DateTime, nullable=True)
    payment_account = db.Column(db.String, nullable=True)

    registration = relationship("Registration", back_populates="invoices")
