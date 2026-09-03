"""Hermes SQLite Kanban Database Engine.

Implements a durable, SQLite-backed task board (kanban.db) matching the official
Nous Research Hermes Agent task architecture with tables:
- boards
- tasks
- task_events
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any

from schemas.kanban_models import KanbanTask, KanbanEvent, TaskStatus, WorkflowStage, KanbanBoardState


class HermesKanbanDB:
    """Durable SQLite Kanban database engine for Hermes agent workflows."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=10.0)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Initialize tables matching Hermes schema specifications."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS boards (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    board_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    assignee TEXT NOT NULL,
                    status TEXT NOT NULL,
                    dependencies TEXT,
                    inputs_summary TEXT,
                    decisions TEXT,
                    outputs_summary TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    agent TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    message TEXT NOT NULL,
                    payload TEXT,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY(task_id) REFERENCES tasks(task_id)
                )
            """)
            conn.commit()

    def ensure_board(self, board_id: str = "cwt_video_ads", name: str = "CrowdWisdomTrading Ads Pipeline") -> None:
        """Ensure the board record exists."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO boards (id, name, description, created_at) VALUES (?, ?, ?, ?)",
                (board_id, name, "Hermes Marketing Video Ads Multi-Agent System", datetime.utcnow().isoformat())
            )
            conn.commit()

    def create_task(self, task: KanbanTask, board_id: str = "cwt_video_ads") -> None:
        """Create or update a task card in the board."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tasks (
                    task_id, board_id, title, stage, assignee, status,
                    dependencies, inputs_summary, decisions, outputs_summary,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    status=excluded.status,
                    inputs_summary=excluded.inputs_summary,
                    decisions=excluded.decisions,
                    outputs_summary=excluded.outputs_summary,
                    updated_at=excluded.updated_at
            """, (
                task.task_id,
                board_id,
                task.title,
                task.stage.value if hasattr(task.stage, 'value') else str(task.stage),
                task.assignee,
                task.status.value if hasattr(task.status, 'value') else str(task.status),
                json.dumps(task.dependencies),
                task.inputs_summary,
                json.dumps(task.decisions),
                task.outputs_summary,
                task.created_at,
                task.updated_at
            ))
            conn.commit()

    def update_task_status(
        self,
        task_id: str,
        status: TaskStatus,
        outputs_summary: Optional[str] = None,
        decision: Optional[str] = None
    ) -> None:
        """Update task status and append decisions/outputs."""
        task = self.get_task(task_id)
        if not task:
            return

        decisions = task.decisions
        if decision:
            decisions.append(decision)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks
                SET status = ?,
                    decisions = ?,
                    outputs_summary = COALESCE(?, outputs_summary),
                    updated_at = ?
                WHERE task_id = ?
            """, (
                status.value if hasattr(status, 'value') else str(status),
                json.dumps(decisions),
                outputs_summary,
                datetime.utcnow().isoformat(),
                task_id
            ))
            conn.commit()

    def get_task(self, task_id: str) -> Optional[KanbanTask]:
        """Fetch a single task by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_task(row)

    def list_tasks(self, board_id: str = "cwt_video_ads") -> List[KanbanTask]:
        """List all tasks ordered by creation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE board_id = ? ORDER BY created_at ASC", (board_id,))
            return [self._row_to_task(row) for row in cursor.fetchall()]

    def log_event(self, event: KanbanEvent) -> None:
        """Record an audit trail event in task_events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO task_events (task_id, agent, event_type, message, payload, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                event.task_id,
                event.agent,
                event.event_type,
                event.message,
                json.dumps(event.payload or {}),
                event.timestamp
            ))
            conn.commit()

    def get_events(self, task_id: Optional[str] = None, limit: int = 50) -> List[KanbanEvent]:
        """Retrieve recent audit events."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if task_id:
                cursor.execute(
                    "SELECT * FROM task_events WHERE task_id = ? ORDER BY event_id DESC LIMIT ?",
                    (task_id, limit)
                )
            else:
                cursor.execute("SELECT * FROM task_events ORDER BY event_id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            return [
                KanbanEvent(
                    event_id=r["event_id"],
                    task_id=r["task_id"],
                    agent=r["agent"],
                    event_type=r["event_type"],
                    message=r["message"],
                    payload=json.loads(r["payload"] or "{}"),
                    timestamp=r["timestamp"]
                ) for r in rows
            ]

    def get_board_state(self, current_stage: WorkflowStage) -> KanbanBoardState:
        """Get aggregate snapshot of current Kanban board."""
        tasks = self.list_tasks()
        total = len(tasks)
        done_count = sum(1 for t in tasks if t.status == TaskStatus.DONE)
        pct = (done_count / total * 100.0) if total > 0 else 0.0
        events = self.get_events(limit=10)
        return KanbanBoardState(
            board_name="CrowdWisdomTrading Ads Pipeline",
            current_stage=current_stage,
            tasks=tasks,
            recent_events=events,
            completion_percentage=round(pct, 1)
        )

    def _row_to_task(self, row: sqlite3.Row) -> KanbanTask:
        return KanbanTask(
            task_id=row["task_id"],
            title=row["title"],
            stage=WorkflowStage(row["stage"]),
            assignee=row["assignee"],
            status=TaskStatus(row["status"]),
            dependencies=json.loads(row["dependencies"] or "[]"),
            inputs_summary=row["inputs_summary"],
            decisions=json.loads(row["decisions"] or "[]"),
            outputs_summary=row["outputs_summary"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
