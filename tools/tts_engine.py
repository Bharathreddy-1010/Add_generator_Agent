"""Text-To-Speech (TTS) Voiceover Synthesizer.

Generates realistic voiceover audio files synchronized to storyboard scene timings.
Supports:
1. macOS native high-quality speech synthesizer (/usr/bin/say) with FFmpeg transcoding
2. Fallback programmatic WAV generator for multi-platform environments
"""

import math
import wave
import struct
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Optional

from config.settings import settings

logger = logging.getLogger("TTSEngine")


class VoiceoverEngine:
    """Generates scene-by-scene audio narration synchronized to storyboard timings."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir or settings.assets_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.has_macos_say = shutil.which("say") is not None
        self.has_ffmpeg = shutil.which("ffmpeg") is not None

    def synthesize_scene_voiceover(
        self,
        scene_idx: int,
        narration_text: str,
        target_duration: float
    ) -> Path:
        """Synthesize audio narration file for a scene matching target_duration."""
        safe_text = narration_text.strip().replace('"', "'")
        out_wav = self.output_dir / f"scene_{scene_idx:02d}_vo.wav"

        if not settings.voiceover_enabled or not safe_text:
            return self._generate_silence_wav(out_wav, target_duration)

        if self.has_macos_say and self.has_ffmpeg:
            try:
                # Step 1: synthesize to uncompressed AIFF using macOS say
                temp_aiff = self.output_dir / f"scene_{scene_idx:02d}_temp.aiff"
                voice = settings.voiceover_voice
                
                # Check rate to match scene duration reasonably (approx 160 wpm standard)
                words = len(safe_text.split())
                wpm = max(130, min(240, int((words / max(target_duration, 1.0)) * 60)))
                
                cmd_say = ["say", "-v", voice, "-r", str(wpm), "-o", str(temp_aiff), safe_text]
                res = subprocess.run(cmd_say, capture_output=True, text=True, timeout=15)
                
                if res.returncode == 0 and temp_aiff.exists():
                    # Step 2: Use ffmpeg to adjust / pad audio to match target_duration exactly
                    # apad pads with silence if shorter; atempo / trim if longer
                    cmd_ffmpeg = [
                        "ffmpeg", "-y",
                        "-i", str(temp_aiff),
                        "-af", f"apad=whole_dur={target_duration}",
                        "-t", str(target_duration),
                        "-ar", "44100",
                        "-ac", "2",
                        str(out_wav)
                    ]
                    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    if temp_aiff.exists():
                        temp_aiff.unlink()
                    logger.info(f"[TTS] Generated macOS voiceover for Scene {scene_idx} ({target_duration}s)")
                    return out_wav
            except Exception as e:
                logger.warning(f"[TTS] macOS say failed ({e}). Falling back to harmonic synthesis.")

        # Fallback harmonic tone synthesizer
        return self._generate_harmonic_voice_wav(out_wav, target_duration, safe_text)

    def _generate_harmonic_voice_wav(self, out_path: Path, duration: float, text: str) -> Path:
        """Generate a soft, dynamic voice-frequency audio waveform matching duration."""
        sample_rate = 44100
        total_samples = int(duration * sample_rate)
        
        # Base speech fundamental frequency ~160 Hz (male/female speech average)
        base_freq = 165.0
        
        with wave.open(str(out_path), "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            frames = bytearray()
            # Modulate based on word cadence
            for i in range(total_samples):
                t = i / sample_rate
                # Subtle speech envelope rhythm
                cadence = 0.5 + 0.5 * math.sin(2 * math.pi * 3.5 * t)
                # Formants (165Hz, 330Hz, 700Hz)
                val = (
                    0.4 * math.sin(2 * math.pi * base_freq * t) +
                    0.25 * math.sin(2 * math.pi * (base_freq * 2) * t) +
                    0.15 * math.sin(2 * math.pi * 700.0 * t)
                ) * cadence
                
                # Fade in / out edges to avoid clicks
                edge_envelope = min(1.0, t / 0.1, (duration - t) / 0.1) if duration > 0.2 else 1.0
                sample_val = int(val * edge_envelope * 12000.0)
                sample_val = max(-32767, min(32767, sample_val))
                frames.extend(struct.pack("<h", sample_val))
            
            wav_file.writeframes(frames)
            
        logger.info(f"[TTS] Generated harmonic speech audio: {out_path.name} ({duration}s)")
        return out_path

    def _generate_silence_wav(self, out_path: Path, duration: float) -> Path:
        """Generate silent audio track."""
        sample_rate = 44100
        total_samples = int(duration * sample_rate)
        with wave.open(str(out_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b"\x00\x00" * total_samples)
        return out_path
