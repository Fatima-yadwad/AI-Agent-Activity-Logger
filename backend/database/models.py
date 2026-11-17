
import uuid

from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    JSON,
    func
)

from sqlalchemy.dialects.postgresql import UUID

from backend.database.connection import Base


class Execution(Base):
    __tablename__ = "executions"

    execution_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_input = Column(Text, nullable=False)
    execution_mode = Column(String(50), nullable=False)
    final_response = Column(Text, nullable=True)

    status = Column(String(30), default="running")

    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    log_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    execution_id = Column(
        UUID(as_uuid=True),
        ForeignKey("executions.execution_id"),
        nullable=False,
        index=True
    )

    event_type = Column(String(50), nullable=False)
    agent_name = Column(String(100), nullable=True)
    action_name = Column(String(100), nullable=True)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True
    )

    status = Column(String(30), default="success")
    duration_ms = Column(Integer, nullable=True)

    details = Column(JSON, default=dict)


class ExecutionMetric(Base):
    __tablename__ = "execution_metrics"

    execution_id = Column(
        UUID(as_uuid=True),
        ForeignKey("executions.execution_id"),
        primary_key=True
    )

    duration_ms = Column(Integer, default=0)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)

    agent_actions = Column(Integer, default=0)
    tool_calls = Column(Integer, default=0)
    agents_involved = Column(Integer, default=0)

    successful_calls = Column(Integer, default=0)
    failed_calls = Column(Integer, default=0)
