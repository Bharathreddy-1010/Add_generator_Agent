"""Pydantic schemas for 30-60 second video-ad storyboards."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, model_validator


class VisualHook(BaseModel):
    """Opening 1-3 second visual pattern interrupt."""
    headline: str = Field(..., description="High-impact punchy hook line")
    visual_description: str = Field(..., description="Action occurring on screen in first 2 seconds")
    audio_cue: str = Field(..., description="Sound effect or sudden drop (e.g. record scratch, freeze)")
    duration_seconds: float = Field(default=3.0, ge=1.0, le=4.0, description="Hook duration")


class Scene(BaseModel):
    """Individual scene within the video storyboard."""
    scene_number: int = Field(..., ge=1)
    start_time: float = Field(..., ge=0.0, description="Start time in seconds")
    end_time: float = Field(..., ge=0.0, description="End time in seconds")
    duration: float = Field(..., ge=0.5, description="Scene duration in seconds")
    visual: str = Field(..., description="Detailed visual direction for animation / scene layout")
    camera: str = Field(..., description="Camera movement: e.g. Static, Zoom In, Fast Pan, Split Screen")
    voiceover: str = Field(..., description="Narration script spoken during this scene")
    on_screen_text: str = Field(..., description="Kinetic typography displayed on screen")
    sound_effect: str = Field(default="none", description="SFX cue (e.g. whoosh, ding, ticker glitch)")
    music: str = Field(default="ambient_electronic", description="Background music energy level")
    transition: str = Field(default="fade", description="Transition to next scene (fade, cut, slide_left, zoom)")


class Storyboard(BaseModel):
    """Complete video storyboard adhering strictly to assessment specifications."""
    ad_id: str
    type: str = Field(..., description="pain_icp, unique_data, or cwt_results")
    title: str
    target_icp: str
    core_pain: str
    marketing_angle: str
    visual_hook: VisualHook
    total_duration_seconds: float = Field(..., ge=20.0, le=65.0)
    scenes: List[Scene] = Field(..., min_length=3)
    cta: str = Field(..., description="Final call to action (verbal and visual)")
    sources: List[str] = Field(default_factory=list, description="Grounding references and citations")

    @model_validator(mode="after")
    def validate_timings(self) -> "Storyboard":
        """Ensure scene durations sum up accurately and sequentially."""
        if not self.scenes:
            raise ValueError("Storyboard must contain at least one scene")
        
        current_time = 0.0
        for s in self.scenes:
            # Allow minor floating tolerance
            if abs(s.start_time - current_time) > 0.5:
                s.start_time = round(current_time, 2)
            if s.duration <= 0:
                s.duration = round(max(1.0, s.end_time - s.start_time), 2)
            s.end_time = round(s.start_time + s.duration, 2)
            current_time = s.end_time
        
        self.total_duration_seconds = round(current_time, 2)
        return self
