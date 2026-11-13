
import pytest

from activity_logging.activity_logger import ActivityLogger


def test_log_user_input():

    logger = ActivityLogger()

    event = logger.log_event(
        execution_id="execution-001",
        event_type="user_input",
        details={
            "content": "Build an AI agent."
        },
        status="received"
    )

    assert event["event_type"] == "user_input"
    assert event["execution_id"] == "execution-001"
    assert event["details"]["content"] == "Build an AI agent."
    assert event["event_id"]
    assert event["timestamp"]


def test_log_agent_action():

    logger = ActivityLogger()

    event = logger.log_event(
        execution_id="execution-001",
        event_type="agent_action",
        details={
            "agent_name": "Requirement Analyst",
            "action": "Analyzed requirements"
        }
    )

    assert event["event_type"] == "agent_action"
    assert event["details"]["agent_name"] == "Requirement Analyst"


def test_log_tool_call():

    logger = ActivityLogger()

    event = logger.log_event(
        execution_id="execution-001",
        event_type="tool_call",
        details={
            "tool_name": "calculator",
            "result": 110
        }
    )

    assert event["event_type"] == "tool_call"
    assert event["details"]["tool_name"] == "calculator"


def test_filter_events_by_execution_id():

    logger = ActivityLogger()

    logger.log_event(
        "execution-001",
        "user_input",
        {"content": "Task A"}
    )

    logger.log_event(
        "execution-002",
        "user_input",
        {"content": "Task B"}
    )

    events = logger.get_events("execution-001")

    assert len(events) == 1
    assert events[0]["execution_id"] == "execution-001"


def test_reject_unknown_event_type():

    logger = ActivityLogger()

    with pytest.raises(ValueError):
        logger.log_event(
            "execution-001",
            "unknown_event",
            {}
        )
