
import uuid

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from backend.database.connection import SessionLocal
from backend.database.models import Execution, ActivityLog, ExecutionMetric
from backend.logging_system.metrics import calculate_metrics


router = APIRouter(
    prefix="/api",
    tags=["Activity Logging"]
)


def execution_to_dict(execution):
    return {
        "execution_id": str(execution.execution_id),
        "user_input": execution.user_input,
        "execution_mode": execution.execution_mode,
        "final_response": execution.final_response,
        "status": execution.status,
        "started_at": (
            execution.started_at.isoformat()
            if execution.started_at else None
        ),
        "completed_at": (
            execution.completed_at.isoformat()
            if execution.completed_at else None
        )
    }


def log_to_dict(log):
    return {
        "log_id": str(log.log_id),
        "execution_id": str(log.execution_id),
        "event_type": log.event_type,
        "agent_name": log.agent_name,
        "action_name": log.action_name,
        "timestamp": log.timestamp.isoformat() if log.timestamp else None,
        "status": log.status,
        "duration_ms": log.duration_ms,
        "details": log.details
    }


@router.get("/executions")
def get_executions():
    db: Session = SessionLocal()

    try:
        executions = db.query(Execution).order_by(
            Execution.started_at.desc()
        ).all()

        return [execution_to_dict(item) for item in executions]

    finally:
        db.close()


@router.get("/executions/{execution_id}")
def get_execution(execution_id: str):
    db = SessionLocal()

    try:
        try:
            execution_id = uuid.UUID(execution_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid execution ID")

        execution = db.query(Execution).filter(
            Execution.execution_id == execution_id
        ).first()

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        logs = db.query(ActivityLog).filter(
            ActivityLog.execution_id == execution_id
        ).order_by(ActivityLog.timestamp.asc()).all()

        metric = calculate_metrics(execution_id)

        return {
            "execution": execution_to_dict(execution),
            "logs": [log_to_dict(log) for log in logs],
            "metrics": metric
        }

    finally:
        db.close()


@router.get("/executions/{execution_id}/logs")
def get_execution_logs(execution_id: str):
    db = SessionLocal()

    try:
        try:
            parsed_id = uuid.UUID(execution_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid execution ID")

        logs = db.query(ActivityLog).filter(
            ActivityLog.execution_id == parsed_id
        ).order_by(ActivityLog.timestamp.asc()).all()

        return [log_to_dict(log) for log in logs]

    finally:
        db.close()


@router.get("/executions/{execution_id}/metrics")
def get_execution_metrics(execution_id: str):
    try:
        return calculate_metrics(execution_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid execution ID")


@router.get("/statistics")
def get_overall_statistics():
    db = SessionLocal()

    try:
        total_executions = db.query(Execution).count()

        successful_executions = db.query(Execution).filter(
            Execution.status == "completed"
        ).count()

        failed_executions = db.query(Execution).filter(
            Execution.status == "failed"
        ).count()

        total_actions = db.query(ActivityLog).filter(
            ActivityLog.event_type == "agent_action"
        ).count()

        total_tools = db.query(ActivityLog).filter(
            ActivityLog.event_type == "tool_call"
        ).count()

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "total_agent_actions": total_actions,
            "total_tool_calls": total_tools
        }

    finally:
        db.close()
