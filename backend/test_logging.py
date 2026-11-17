
import uuid

from backend.database.connection import SessionLocal
from backend.database.models import Execution

from backend.logging_system.logger import log_event
from backend.logging_system.tracer import ExecutionTracer
from backend.logging_system.metrics import calculate_metrics


def test_logging():

    execution_id = uuid.uuid4()

    # Create an execution
    db = SessionLocal()

    try:
        execution = Execution(
            execution_id=execution_id,
            user_input="Calculate 25% of 800",
            execution_mode="conversation",
            status="running"
        )

        db.add(execution)
        db.commit()

    finally:
        db.close()

    # Start tracing
    tracer = ExecutionTracer(execution_id)
    tracer.start()

    # Record events
    tracer.record(
        event_type="user_input",
        details={"input": "Calculate 25% of 800"}
    )

    tracer.record(
        event_type="agent_action",
        agent_name="RequirementAnalyst",
        action_name="analyze_request",
        details={"description": "Analyzing calculation request"}
    )

    tracer.record(
        event_type="tool_call",
        agent_name="RequirementAnalyst",
        action_name="calculator",
        details={"expression": "800 * 0.25"}
    )

    tracer.record(
        event_type="tool_result",
        agent_name="RequirementAnalyst",
        action_name="calculator",
        details={"result": 200}
    )

    # Complete execution
    tracer.finish(
        final_response="25% of 800 is 200.",
        status="completed"
    )

    # Calculate metrics
    metrics = calculate_metrics(execution_id)

    print("\n========== EXECUTION METRICS ==========")
    print(metrics)

    print("\n========== TEST COMPLETED ==========")


if __name__ == "__main__":
    test_logging()
