
import time
import uuid

from datetime import datetime, timezone

from backend.database.connection import SessionLocal
from backend.database.models import Execution

from backend.logging_system.logger import log_event
from backend.logging_system.metrics import calculate_metrics


class ExecutionTracer:

    def __init__(self, execution_id):
        self.execution_id = uuid.UUID(str(execution_id))
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def record(
        self,
        event_type,
        agent_name=None,
        action_name=None,
        status="success",
        details=None,
        duration_ms=None
    ):
        return log_event(
            execution_id=self.execution_id,
            event_type=event_type,
            agent_name=agent_name,
            action_name=action_name,
            status=status,
            details=details,
            duration_ms=duration_ms
        )

    def finish(self, final_response=None, status="completed"):
        if self.start_time is None:
            raise RuntimeError("Tracer has not been started")

        duration = round(
            (time.perf_counter() - self.start_time) * 1000
        )

        db = SessionLocal()

        try:
            execution = db.query(Execution).filter(
                Execution.execution_id == self.execution_id
            ).first()

            if execution:
                execution.status = status
                execution.final_response = final_response
                execution.completed_at = datetime.now(timezone.utc)

                db.commit()

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()

        log_event(
            execution_id=self.execution_id,
            event_type="execution_completed" if status == "completed"
                       else "execution_failed",
            status="success" if status == "completed" else "error",
            details={"duration_ms": duration},
            duration_ms=duration
        )

        calculate_metrics(self.execution_id)

        return duration
