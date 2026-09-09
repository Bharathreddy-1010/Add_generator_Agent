"""Application Configuration using Pydantic Settings.

Supports DEMO_MODE, OpenRouter/NVIDIA LLM providers, Apify, Tavily, Exa,
and output directory management.
"""

from pathlib import Path
from typing import Optional, Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Runtime mode
    demo_mode: bool = Field(default=True, description="Run with verified fixtures without external API calls")
    debug_logging: bool = Field(default=False, description="Enable verbose debug logging")

    # LLM Provider
    llm_provider: Literal["openrouter", "nvidia"] = Field(
        default="openrouter",
        description="LLM provider: openrouter or nvidia"
    )
    openrouter_api_key: Optional[str] = Field(default=None, description="OpenRouter API Key")
    openrouter_model: str = Field(default="meta-llama/llama-3.3-70b-instruct", description="Model name on OpenRouter")

    nvidia_api_key: Optional[str] = Field(default=None, description="NVIDIA Build API Key")
    nvidia_model: str = Field(default="meta/llama-3.3-70b-instruct", description="Model name on NVIDIA Build")
    nvidia_base_url: str = Field(default="https://integrate.api.nvidia.com/v1", description="NVIDIA API base URL")

    # Scraping & Search APIs
    apify_api_token: Optional[str] = Field(default=None, description="Apify API Token")
    tavily_api_key: Optional[str] = Field(default=None, description="Tavily API Key")
    exa_api_key: Optional[str] = Field(default=None, description="Exa API Key")

    # Video & Voiceover
    video_width: int = Field(default=1080, description="Ad width (9:16 vertical)")
    video_height: int = Field(default=1920, description="Ad height (9:16 vertical)")
    video_fps: int = Field(default=30, description="Target frames per second")
    voiceover_enabled: bool = Field(default=True, description="Generate audio narration")
    voiceover_voice: str = Field(default="en-US-ChristopherNeural", description="TTS voice name: edge-tts neural voice or macOS male voice")

    # Base Paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def ads_dir(self) -> Path:
        return self.data_dir / "ads"

    @property
    def raw_ads_dir(self) -> Path:
        return self.ads_dir / "raw"

    @property
    def analysis_dir(self) -> Path:
        return self.data_dir / "analysis"

    @property
    def research_dir(self) -> Path:
        return self.data_dir / "research"

    @property
    def scripts_dir(self) -> Path:
        return self.data_dir / "scripts"

    @property
    def crowdwisdom_dir(self) -> Path:
        return self.data_dir / "crowdwisdom"

    @property
    def fixtures_dir(self) -> Path:
        return self.data_dir / "fixtures"

    @property
    def outputs_dir(self) -> Path:
        return self.base_dir / "outputs"

    @property
    def assets_dir(self) -> Path:
        return self.outputs_dir / "assets"

    @property
    def renders_dir(self) -> Path:
        return self.outputs_dir / "renders"

    @property
    def kanban_db_path(self) -> Path:
        return self.data_dir / "kanban.db"

    def ensure_directories(self) -> None:
        """Create all required runtime directory structures."""
        dirs = [
            self.data_dir,
            self.ads_dir,
            self.raw_ads_dir,
            self.analysis_dir,
            self.research_dir,
            self.scripts_dir,
            self.crowdwisdom_dir,
            self.fixtures_dir,
            self.outputs_dir,
            self.assets_dir,
            self.renders_dir,
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)


# Global singleton settings instance
settings = Settings()
