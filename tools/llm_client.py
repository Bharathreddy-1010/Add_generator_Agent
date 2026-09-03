"""LLM Client supporting OpenRouter and NVIDIA Build with structured JSON generation.

Includes prompt structuring, JSON schema validation, retry logic, and fallback responses
for local demo and offline test environments.
"""

import json
import logging
from typing import Type, TypeVar, Optional, Dict, Any
from pydantic import BaseModel
from openai import OpenAI

from config.settings import settings

logger = logging.getLogger("LLMClient")
T = TypeVar("T", bound=BaseModel)


class StructuredLLMClient:
    """Unified OpenAI-compatible client for OpenRouter and NVIDIA Build."""

    def __init__(self):
        self.provider = settings.llm_provider
        self.client: Optional[OpenAI] = None
        self._init_client()

    def _init_client(self) -> None:
        if settings.demo_mode:
            logger.info("[LLMClient] Running in DEMO_MODE: External LLM calls bypassed.")
            return

        if self.provider == "nvidia":
            if settings.nvidia_api_key:
                self.client = OpenAI(
                    base_url=settings.nvidia_base_url,
                    api_key=settings.nvidia_api_key
                )
                self.model = settings.nvidia_model
                logger.info(f"[LLMClient] Initialized NVIDIA Build client with model: {self.model}")
            else:
                logger.warning("[LLMClient] NVIDIA_API_KEY missing. Falling back to local offline mode.")
        else:
            # Default to OpenRouter
            if settings.openrouter_api_key:
                self.client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=settings.openrouter_api_key
                )
                self.model = settings.openrouter_model
                logger.info(f"[LLMClient] Initialized OpenRouter client with model: {self.model}")
            else:
                logger.warning("[LLMClient] OPENROUTER_API_KEY missing. Falling back to local offline mode.")

    def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[T],
        fallback_factory: Optional[callable] = None,
        max_retries: int = 2
    ) -> T:
        """Call LLM and parse response into validated Pydantic model T."""
        if settings.demo_mode or not self.client:
            if fallback_factory:
                return fallback_factory()
            raise ValueError("No LLM client available and no fallback factory provided.")

        system_instruction = (
            f"{system_prompt}\n\n"
            "CRITICAL INSTRUCTIONS:\n"
            "1. Output ONLY valid, parseable JSON matching the requested schema.\n"
            "2. Do NOT wrap output in markdown codeblocks (no ```json).\n"
            "3. Do NOT hallucinate financial performance or fake promises.\n"
            "4. Be strictly grounded in the provided factual context."
        )

        for attempt in range(max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3,
                )
                content = response.choices[0].message.content.strip()
                # Clean any stray codeblock formatting if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                parsed_json = json.loads(content)
                return response_model.model_validate(parsed_json)

            except Exception as e:
                logger.warning(f"[LLMClient] Generation attempt {attempt + 1} failed: {e}")
                if attempt == max_retries:
                    if fallback_factory:
                        logger.info("[LLMClient] Returning fallback model after retries.")
                        return fallback_factory()
                    raise e
