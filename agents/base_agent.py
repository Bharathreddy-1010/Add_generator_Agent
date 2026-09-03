"""Base Agent class defining interface for Hermes-orchestrated agents."""

import logging
from abc import ABC, abstractmethod
from typing import Optional

from hermes.workflow import HermesWorkflowOrchestrator
from config.settings import settings


class BaseAgent(ABC):
    """Abstract base class for all marketing and creative pipeline agents."""

    def __init__(self, name: str, workflow: Optional[HermesWorkflowOrchestrator] = None):
        self.name = name
        self.workflow = workflow
        self.settings = settings
        self.logger = logging.getLogger(name)

    def log_status(self, task_id: str, message: str) -> None:
        if self.workflow:
            self.workflow.log_status(task_id, self.name, message)
        else:
            self.logger.info(f"[{self.name}] {message}")

    def log_decision(self, task_id: str, decision: str) -> None:
        if self.workflow:
            self.workflow.log_decision(task_id, self.name, decision)
        else:
            self.logger.info(f"[{self.name}] Decision: {decision}")

    @abstractmethod
    def run(self, *args, **kwargs):
        """Execute the agent's core responsibility."""
        pass
