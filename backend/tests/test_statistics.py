
from activity_logging.activity_logger import ActivityLogger


def test_empty_statistics():

    logger = ActivityLogger()

    stats = logger.get_statistics()

    assert stats["total_executions"] == 0
    assert stats["total_events"] == 0
    assert stats["total_tokens"] == 0
    assert stats["average_response_time_ms"] == 0


def test_execution_statistics():

    logger = ActivityLogger()

    execution_id = "execution-001"

    logger.log_event(
        execution_id,
        "user_input",
        {"content": "Build an AI agent."},
        "received"
    )

    logger.log_event(
        execution_id,
        "agent_action",
        {"agent_name": "Requirement Analyst"}
    )

    logger.log_event(
        execution_id,
        "execution_completed",
        {
            "duration_ms": 120.0,
            "total_tokens": 150
        }
    )

    stats = logger.get_statistics()

    assert stats["total_executions"] == 1
    assert stats["successful_executions"] == 1
    assert stats["user_inputs"] == 1
    assert stats["agent_actions"] == 1
    assert stats["total_tokens"] == 150
    assert stats["average_response_time_ms"] == 120.0


def test_multiple_executions():

    logger = ActivityLogger()

    logger.log_event(
        "execution-001",
        "execution_completed",
        {
            "duration_ms": 100.0,
            "total_tokens": 100
        }
    )

    logger.log_event(
        "execution-002",
        "execution_completed",
        {
            "duration_ms": 200.0,
            "total_tokens": 200
        }
    )

    stats = logger.get_statistics()

    assert stats["total_executions"] == 2
    assert stats["total_tokens"] == 300
    assert stats["average_response_time_ms"] == 150.0
    assert stats["fastest_execution_ms"] == 100.0
    assert stats["slowest_execution_ms"] == 200.0


def test_failed_execution_statistics():

    logger = ActivityLogger()

    logger.log_event(
        "execution-001",
        "execution_failed",
        {
            "duration_ms": 50.0,
            "error": "Test failure"
        },
        status="failed"
    )

    stats = logger.get_statistics()

    assert stats["total_executions"] == 1
    assert stats["failed_executions"] == 1
    assert stats["successful_executions"] == 0
