
import uuid
from datetime import datetime, timezone

from backend.database.connection import SessionLocal
from backend.database.models import ActivityLog


def log_event(
    execution_id,
    event_type,
    status="success",
    agent_name=None,
    action_name=None,
    details=None,
    duration_ms=None
):
    db = SessionLocal()

    try:
        event = ActivityLog(
            log_id=uuid.uuid4(),
            execution_id=uuid.UUID(str(execution_id)),
            event_type=event_type,
            status=status,
            agent_name=agent_name,
            action_name=action_name,
            timestamp=datetime.now(timezone.utc),
            details=details or {},
            duration_ms=duration_ms
        )

        db.add(event)
        db.commit()
        db.refresh(event)

        print(f"LOG RECORDED: {event_type}")

        return event

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
