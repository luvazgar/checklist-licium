from __future__ import annotations
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UUID
from app.core.base import Base
from app.core.fields import field



class Registration(Base):
    __tablename__ = "community_events_registration"
    __abstract__ = False
    __model__ = "registration"
    __service__ = "modules.community_events.services.registration.RegistrationService"

    event_id = field(
        Integer,
        ForeignKey("community_events_event.id", ondelete="CASCADE"),
        required=True,
        public=True,
        editable=True,
        info = {"label": "ID del evento"}
        )


    session_id = field(
        Integer,
        ForeignKey("community_events_session.id", ondelete="SET NULL"),
        required=False,
        public=True,
        editable=True,
        info = {"label": "ID de la sesión"}
        )


    attendee_name = field(
        String(150),
        required=True,
        public=True,
        editable=True,
        info = {"label": "Nombre del asistente/a"}
        )


    attendee_email = field(
        String(150),
        required=True,
        public=True,
        editable=True,
        info = {"label": "Email del asistente/a"}
        )


    attendee_user_id = field(
        UUID,
        ForeignKey("core_user.id", ondelete="SET NULL"),
        required=False,
        public=True,
        editable=True,
        info = {"label": "Usuario del asistente/a"}
        )


    status = field(
        String(20),
        required=True,
        default="pending",
        public=True,
        editable=True,
        info={"choices": [
            {"label": "Pendiente", "value": "pending"},
            {"label": "Confirmado", "value": "confirmed"},
            {"label": "En lista de Espera", "value": "waitlist"},
            {"label": "Cancelado", "value": "cancelled"}
        ]}
    )


    registered_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=False,
        info = {"label": "Fecha de registro(dd/mm/aaaa)"}
        )


    checkin_at = field(
        DateTime(timezone=True),
        required=False,
        public=True,
        editable=False,
        info = {"label": "Fecha de check-in(dd/mm/aaaa)"}
        )


    notes = field(
        Text,
        required=False,
        public=True,
        editable=True,
        info = {"label": "Notas del registro"}
        )