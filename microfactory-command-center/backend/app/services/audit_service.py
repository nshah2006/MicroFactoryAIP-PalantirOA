from app.models.audit_event import AuditEvent


def log_event(db, event_type: str, entity_type: str, entity_id: str, message: str, actor="System", role="System", before_state=None, after_state=None):
    event = AuditEvent(
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        actor=actor,
        role=role,
        message=message,
        before_state=before_state,
        after_state=after_state,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
