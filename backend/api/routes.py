
import time
import uuid

from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from activity_logging.activity_logger import ActivityLogger

from services.gemini_service import GeminiService

from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent

from orchestrator.conversation import ConversationOrchestrator
from orchestrator.round_robin import RoundRobinOrchestrator
from orchestrator.selector import SelectorOrchestrator

from tools.calculator import CalculatorTool
from tools.tool_registry import ToolRegistry


# --------------------------------------------------
# API INITIALIZATION
# --------------------------------------------------

router = APIRouter(
    prefix="/api",
    tags=["Agent Execution"]
)

gemini = GeminiService()

activity_logger = ActivityLogger()

tool_registry = ToolRegistry()
tool_registry.register("calculator", CalculatorTool())


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class ExecuteRequest(BaseModel):

    task: str = Field(
        min_length=1,
        max_length=10000
    )

    mode: Literal[
        "conversation",
        "round_robin",
        "selector"
    ] = "conversation"

    rounds: int = Field(
        default=1,
        ge=1,
        le=10
    )


class ToolExecuteRequest(BaseModel):

    tool_name: str = Field(
        min_length=1
    )

    arguments: dict = Field(
        default_factory=dict
    )


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def current_timestamp():

    return datetime.now(
        timezone.utc
    ).isoformat()


def calculate_duration(start_time):

    return round(
        (time.perf_counter() - start_time) * 1000,
        2
    )


# --------------------------------------------------
# AGENT EXECUTION ENDPOINT
# --------------------------------------------------

@router.post("/execute")
async def execute_agent(request: ExecuteRequest):

    execution_id = str(uuid.uuid4())

    timestamp = current_timestamp()

    start_time = time.perf_counter()

    try:

        # Record original user input
        activity_logger.log_event(
            execution_id=execution_id,
            event_type="user_input",
            details={
                "content": request.task,
                "mode": request.mode,
                "rounds": request.rounds
            },
            status="received"
        )

        # ------------------------------------------
        # CONVERSATION MODE
        # ------------------------------------------

        if request.mode == "conversation":

            orchestrator = ConversationOrchestrator(
                gemini
            )

            result = await orchestrator.execute(
                task=request.task
            )

        # ------------------------------------------
        # ROUND ROBIN MODE
        # ------------------------------------------

        elif request.mode == "round_robin":

            agents = [
                RequirementAgent(gemini),
                ArchitectAgent(gemini)
            ]

            orchestrator = RoundRobinOrchestrator(
                agents
            )

            result = await orchestrator.execute(
                task=request.task,
                rounds=request.rounds
            )

        # ------------------------------------------
        # SELECTOR MODE
        # ------------------------------------------

        elif request.mode == "selector":

            orchestrator = SelectorOrchestrator(
                gemini
            )

            result = await orchestrator.execute(
                task=request.task
            )

        else:

            raise HTTPException(
                status_code=400,
                detail="Unsupported execution mode"
            )

        # ------------------------------------------
        # RECORD AGENT ACTIONS
        # ------------------------------------------

        for event in result["events"]:

            activity_logger.log_event(
                execution_id=execution_id,
                event_type="agent_action",
                details=event,
                status=event.get(
                    "status",
                    "completed"
                )
            )

        # ------------------------------------------
        # EXECUTION METRICS
        # ------------------------------------------

        duration_ms = calculate_duration(
            start_time
        )

        usage = result["usage"]

        # Record successful execution
        activity_logger.log_event(
            execution_id=execution_id,
            event_type="execution_completed",
            details={
                "mode": request.mode,
                "duration_ms": duration_ms,
                "total_tokens": usage["total_tokens"]
            },
            status="completed"
        )

        # Retrieve complete execution trace
        events = activity_logger.get_events(
            execution_id
        )

        # ------------------------------------------
        # API RESPONSE
        # ------------------------------------------

        return {
            "execution_id": execution_id,
            "timestamp": timestamp,
            "task": request.task,
            "mode": request.mode,
            "status": "completed",
            "duration_ms": duration_ms,
            "results": result["results"],
            "events": events,
            "usage": usage
        }

    except HTTPException:
        raise

    except Exception as exc:

        duration_ms = calculate_duration(
            start_time
        )

        activity_logger.log_event(
            execution_id=execution_id,
            event_type="execution_failed",
            details={
                "error": str(exc),
                "duration_ms": duration_ms
            },
            status="failed"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(exc)}"
        )


# --------------------------------------------------
# TOOL LIST ENDPOINT
# --------------------------------------------------

@router.get("/tools")
def list_tools():

    return {
        "tools": tool_registry.list_tools()
    }


# --------------------------------------------------
# TOOL EXECUTION ENDPOINT
# --------------------------------------------------

@router.post("/tools/execute")
def execute_tool(request: ToolExecuteRequest):

    execution_id = str(uuid.uuid4())

    timestamp = current_timestamp()

    start_time = time.perf_counter()

    try:

        # Execute the actual registered tool
        result = tool_registry.execute(
            request.tool_name,
            **request.arguments
        )

        duration_ms = calculate_duration(
            start_time
        )

        # Record actual tool invocation
        activity_logger.log_event(
            execution_id=execution_id,
            event_type="tool_call",
            details={
                "tool_name": request.tool_name,
                "arguments": request.arguments,
                "result": result,
                "duration_ms": duration_ms
            },
            status="completed"
        )

        events = activity_logger.get_events(
            execution_id
        )

        return {
            "execution_id": execution_id,
            "timestamp": timestamp,
            "status": "completed",
            "result": result,
            "duration_ms": duration_ms,
            "events": events
        }

    except (ValueError, TypeError) as exc:

        activity_logger.log_event(
            execution_id=execution_id,
            event_type="tool_call",
            details={
                "tool_name": request.tool_name,
                "arguments": request.arguments,
                "error": str(exc)
            },
            status="failed"
        )

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Tool execution failed: {str(exc)}"
        )


# --------------------------------------------------
# ACTIVITY LOG RETRIEVAL ENDPOINT
# --------------------------------------------------

@router.get("/logs")
def get_activity_logs(
    execution_id: str | None = Query(
        default=None
    )
):

    events = activity_logger.get_events(
        execution_id
    )

    return {
        "total_events": len(events),
        "events": events
    }


@router.get("/statistics")
def get_execution_statistics():

    return activity_logger.get_statistics()
