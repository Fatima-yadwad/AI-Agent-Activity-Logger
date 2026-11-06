
import uuid

from sqlalchemy import func

from backend.database.connection import SessionLocal
from backend.database.models import (
    ActivityLog,
    Execution,
    ExecutionMetric
)


def calculate_metrics(execution_id):
    execution_id = uuid.UUID(str(execution_id))

    db = SessionLocal()

    try:
        actions = db.query(ActivityLog).filter(
            ActivityLog.execution_id == execution_id,
            ActivityLog.event_type == "agent_action"
        ).count()

        tools = db.query(ActivityLog).filter(
            ActivityLog.execution_id == execution_id,
            ActivityLog.event_type == "tool_call"
        ).count()

        successful = db.query(ActivityLog).filter(
            ActivityLog.execution_id == execution_id,
            ActivityLog.event_type == "tool_result",
            ActivityLog.status == "success"
        ).count()

        failed = db.query(ActivityLog).filter(
            ActivityLog.execution_id == execution_id,
            ActivityLog.status == "error"
        ).count()

        agents = db.query(
            func.count(func.distinct(ActivityLog.agent_name))
        ).filter(
            ActivityLog.execution_id == execution_id,
            ActivityLog.agent_name.isnot(None)
        ).scalar() or 0

        execution = db.query(Execution).filter(
            Execution.execution_id == execution_id
        ).first()

        duration = 0

        if execution and execution.completed_at and execution.started_at:
            duration = int(
                (execution.completed_at - execution.started_at)
                .total_seconds() * 1000
            )

        metric = db.query(ExecutionMetric).filter(
            ExecutionMetric.execution_id == execution_id
        ).first()

        if not metric:
            metric = ExecutionMetric(execution_id=execution_id)
            db.add(metric)

        metric.agent_actions = actions
        metric.tool_calls = tools
        metric.successful_calls = successful
        metric.failed_calls = failed
        metric.agents_involved = agents
        metric.duration_ms = duration

        db.commit()

        return {
            "execution_id": str(execution_id),
            "duration_ms": duration,
            "agent_actions": actions,
            "tool_calls": tools,
            "successful_calls": successful,
            "failed_calls": failed,
            "agents_involved": agents,
            "input_tokens": metric.input_tokens,
            "output_tokens": metric.output_tokens,
            "total_tokens": metric.total_tokens
        }

    finally:
        db.close()
