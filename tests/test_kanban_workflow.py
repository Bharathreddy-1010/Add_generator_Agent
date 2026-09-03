"""Tests for Hermes SQLite Kanban DB and Workflow Orchestrator."""

import pytest
from pathlib import Path
from hermes.kanban_db import HermesKanbanDB
from hermes.workflow import HermesWorkflowOrchestrator
from schemas.kanban_models import TaskStatus, WorkflowStage, KanbanTask, KanbanEvent


def test_kanban_db_operations(tmp_path):
    db_file = tmp_path / "test_kanban.db"
    db = HermesKanbanDB(db_file)
    db.ensure_board()

    # Create task
    task = KanbanTask(
        task_id="t_test",
        title="Test Task",
        stage=WorkflowStage.RESEARCHING_ADS,
        assignee="AdsManager",
        status=TaskStatus.TODO
    )
    db.create_task(task)

    fetched = db.get_task("t_test")
    assert fetched is not None
    assert fetched.status == TaskStatus.TODO

    # Update status
    db.update_task_status("t_test", TaskStatus.IN_PROGRESS, decision="Selected strategy")
    updated = db.get_task("t_test")
    assert updated.status == TaskStatus.IN_PROGRESS
    assert "Selected strategy" in updated.decisions

    # Log event
    db.log_event(KanbanEvent(
        task_id="t_test",
        agent="AdsManager",
        event_type="START",
        message="Started test"
    ))
    events = db.get_events(task_id="t_test")
    assert len(events) == 1
    assert events[0].event_type == "START"
