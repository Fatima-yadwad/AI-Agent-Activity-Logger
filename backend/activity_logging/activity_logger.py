
from datetime import datetime, timezone
from uuid import uuid4


class ActivityLogger:

    def __init__(self):
        self.events = []

    def log_event(
        self,
        execution_id: str,
        event_type: str,
        details: dict,
        status: str = "completed"
    ) -> dict:

        allowed_types = {
            "user_input",
            "agent_action",
            "tool_call",
            "execution_completed",
            "execution_failed"
        }

        if event_type not in allowed_types:
            raise ValueError(
                f"Unsupported event type: {event_type}"
            )

        event = {
            "event_id": str(uuid4()),
            "execution_id": execution_id,
            "event_type": event_type,
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "status": status,
            "details": details
        }

        self.events.append(event)

        return event

    def get_events(self, execution_id=None):

        if execution_id is None:
            return list(self.events)

        return [
            event
            for event in self.events
            if event["execution_id"] == execution_id
        ]

    def get_statistics(self):

        events = self.events

        execution_events = [
            event for event in events
            if event["event_type"] in {
                "execution_completed",
                "execution_failed"
            }
        ]

        execution_ids = {
            event["execution_id"]
            for event in execution_events
        }

        durations = [
            event["details"]["duration_ms"]
            for event in execution_events
            if "duration_ms" in event["details"]
        ]

        total_tokens = sum(
            event["details"].get("total_tokens", 0)
            for event in events
            if event["event_type"] == "execution_completed"
        )

        return {
            "total_executions": len(execution_ids),

            "successful_executions": sum(
                event["event_type"] == "execution_completed"
                for event in execution_events
            ),

            "failed_executions": sum(
                event["event_type"] == "execution_failed"
                for event in execution_events
            ),

            "total_events": len(events),

            "user_inputs": sum(
                event["event_type"] == "user_input"
                for event in events
            ),

            "agent_actions": sum(
                event["event_type"] == "agent_action"
                for event in events
            ),

            "tool_calls": sum(
                event["event_type"] == "tool_call"
                for event in events
            ),

            "total_tokens": total_tokens,

            "average_response_time_ms": (
                round(sum(durations) / len(durations), 2)
                if durations else 0
            ),

            "fastest_execution_ms": (
                min(durations) if durations else 0
            ),

            "slowest_execution_ms": (
                max(durations) if durations else 0
            )
        }

    def clear(self):
        self.events.clear()
