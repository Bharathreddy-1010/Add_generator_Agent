"""Pydantic schemas for Hermes SQLite-backed Kanban boards, tasks, and event lifecycle."""

from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"


class WorkflowStage(str, Enum):
    INITIALIZE = "INITIALIZE"
    RESEARCHING_ADS = "RESEARCHING_ADS"
    ANALYZING_ADS = "ANALYZING_ADS"
    RESEARCHING_ICP = "RESEARCHING_ICP"
    GENERATING_SCRIPTS = "GENERATING_SCRIPTS"
    EVALUATING_CONCEPTS = "EVALUATING_CONCEPTS"
    GENERATING_VIDEO = "GENERATING_VIDEO"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class KanbanTask(BaseModel):
    """Hermes Kanban Task representation."""
    task_id: str
    title: str
    stage: WorkflowStage
    assignee: str = Field(..., description="Agent profile assigned: e.g. AdsManager, ScriptAgent")
    status: TaskStatus = Field(default=TaskStatus.TODO)
    dependencies: List[str] = Field(default_factory=list)
    inputs_summary: Optional[str] = None
    decisions: List[str] = Field(default_factory=list)
    outputs_summary: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KanbanEvent(BaseModel):
    """Audit log event emitted by agents during execution."""
    event_id: Optional[int] = None
    task_id: str
    agent: str
    event_type: str = Field(..., description="START, STATUS, DECISION, OUTPUT, ERROR, COMPLETE")
    message: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KanbanBoardState(BaseModel):
    """Snapshot of current Kanban board."""
    board_name: str = "CrowdWisdomTrading Video Ads Pipeline"
    current_stage: WorkflowStage
    tasks: List[KanbanTask]
    recent_events: List[KanbanEvent] = Field(default_factory=list)
    completion_percentage: float = 0.0
