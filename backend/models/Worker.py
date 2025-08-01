from extensions import db
from enum import Enum
from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_serializer import SerializerMixin
from models.association import worker_skills
import models.Skill

class WorkerStatus(Enum):
    REQUESTS = 'requests'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    DEACTIVATED = 'deactivated'
    REACTIVATED = 'reactivated'

    
class Worker(db.Model, SerializerMixin):
    __tablename__ = 'workers'

    worker_id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(db.ForeignKey('clients.client_id'), nullable=False)

    bio: Mapped[str] = mapped_column(db.Text, nullable=True)
    id_number = db.Column(db.String(50), nullable=False)
    hourly_rate: Mapped[float] = mapped_column(db.Float, nullable=False, default=0.0)
    location: Mapped[str] = mapped_column(db.String(120), nullable=False)
    status: Mapped[WorkerStatus] = mapped_column(
        db.Enum(
            WorkerStatus,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
            name="workerstatus"
        ),
        nullable=False,
        default=WorkerStatus.REQUESTS 
    )
    experience_years = db.Column(db.Integer, nullable=True)
    certificate_url = db.Column(db.String, nullable=True)  # store file URL
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    is_verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(db.Boolean, default=False)
    is_approved: Mapped[bool] = mapped_column(default=False)

    # Relationships
    client = relationship('Client', back_populates='workers')
    jobs = relationship('Job', back_populates='worker', cascade='all, delete-orphan')
    portfolio = relationship('WorkerPortfolio', back_populates='worker', cascade='all, delete-orphan')

    skills: Mapped[List["Skill"]] = relationship(
        "Skill",
        secondary=worker_skills,
        back_populates="workers"
    )
    #skills = db.relationship("Skill", secondary=worker_skills, back_populates="workers")


    serialize_rules = ('-client.workers', '-client.jobs', '-client.hashed_password',)

    def __repr__(self):
        return f'<Worker {self.worker_id}>'
