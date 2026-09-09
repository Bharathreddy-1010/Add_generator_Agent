"""Text-To-Speech (TTS) Voiceover Synthesizer.

Generates realistic, interactive male voiceover audio files synchronized to storyboard scenes.
Supports:
1. Neural edge-tts synthesizer (e.g. en-US-ChristopherNeural, en-US-GuyNeural) for
   broadcast-grade documentary and performance-marketing delivery
2. macOS native speech synthesizer (/usr/bin/say) with male voices (Daniel, Oliver, Alex) as fallback
3. Programmatic harmonic audio synthesizer for offline environments
4. Frame-accurate audio duration measurement for 100% audio-video synchronization
"""

import math
import wave
import struct
import shutil
import logging
import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import numpy as np

from config.settings import settings

logger = logging.getLogger("TTSEngine")


class VoiceoverEngine:
    """Generates scene-by-scene interactive audio narration and measures exact duration."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir or settings.assets_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.has_macos_say = shutil.which("say") is not None
        self.has_ffmpeg = shutil.which("ffmpeg") is not None
        self.last_measured_duration: float = 0.0

    def get_audio_duration(self, audio_path: Path) -> float:
        """Return the exact duration in seconds of a WAV or audio file."""
        if not audio_path.exists():
            return 0.0
        # Fast path for WAV files
        try:
            with wave.open(str(audio_path), "rb") as wf:
                frames = wf.getnframes()
                rate = wf.getframerate()
                if rate > 0:
                    return round(frames / float(rate), 3)
        except Exception:
            pass

        # Fallback to ffprobe
        if self.has_ffmpeg:
            try:
                cmd = [
                    "ffprobe", "-v", "error",
                    "-show_entries", "format=duration",
                    "-of", "default=noprint_wrappers=1:nokey=1",
                    str(audio_path)
                ]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return round(float(res.stdout.strip()), 3)
            except Exception as e:
                logger.warning(f"Could not probe audio duration: {e}")
        return 0.0

    def synthesize_scene_voiceover(
        self,
        scene_idx: int,
        narration_text: str,
        target_duration: Optional[float] = None
    ) -> Path:
        """Synthesize audio narration file for a scene and return the WAV file path.
        
        Saves exact duration in self.last_measured_duration.
        """
        wav_path, duration = self.synthesize_and_measure(
            scene_idx=scene_idx,
            narration_text=narration_text,
            target_duration=target_duration
        )
        return wav_path

    def synthesize_and_measure(
        self,
        scene_idx: int,
        narration_text: str,
        target_duration: Optional[float] = None
    ) -> Tuple[Path, float]:
        """Synthesize interactive male narration and measure exact duration in seconds."""
        safe_text = narration_text.strip().replace('"', "'")
        out_wav = self.output_dir / f"scene_{scene_idx:02d}_vo.wav"

        if not settings.voiceover_enabled or not safe_text:
            duration = target_duration or 3.0
            self._generate_silence_wav(out_wav, duration)
            self.last_measured_duration = duration
            return out_wav, duration

        # 1. Primary Engine: edge-tts (high fidelity interactive male voice)
        voice_name = settings.voiceover_voice
        if not voice_name or voice_name.lower() in ("samantha", "default"):
            voice_name = "en-US-ChristopherNeural"

        try:
            temp_mp3 = self.output_dir / f"scene_{scene_idx:02d}_temp.mp3"
            
            # Use edge-tts directly via Python asyncio
            import edge_tts

            async def _run_edge_tts():
                communicate = edge_tts.Communicate(
                    text=safe_text,
                    voice=voice_name,
                    rate="+4%",  # Punchy, engaging marketing cadence
                    pitch="+0Hz"
                )
                await communicate.save(str(temp_mp3))

            asyncio.run(_run_edge_tts())

            if temp_mp3.exists() and temp_mp3.stat().st_size > 500:
                # Transcode MP3 to high-quality 44.1kHz stereo WAV
                cmd_ffmpeg = [
                    "ffmpeg", "-y",
                    "-i", str(temp_mp3),
                    "-ar", "44100",
                    "-ac", "2",
                    str(out_wav)
                ]
                subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                if temp_mp3.exists():
                    temp_mp3.unlink()

                # Trim trailing silence with crisp 0.25s breathing room for instant, punchy scene cuts
                duration = self._trim_trailing_silence(out_wav, pad_end_sec=0.25)
                self.last_measured_duration = duration
                logger.info(f"[TTS] Synthesized edge-tts male voice for Scene {scene_idx}: {duration}s ('{voice_name}')")
                return out_wav, duration
        except Exception as e:
            logger.warning(f"[TTS] edge-tts synthesis failed ({e}). Falling back to macOS native speech.")

        # 2. Fallback Engine: macOS native speech synthesizer (/usr/bin/say) with male voice
        if self.has_macos_say and self.has_ffmpeg:
            try:
                temp_aiff = self.output_dir / f"scene_{scene_idx:02d}_temp.aiff"
                
                # Check for male voices on macOS: Daniel, Oliver, Alex, Rocko
                macos_voice = "Daniel"
                words = len(safe_text.split())
                wpm = 175  # Natural documentary speaking rate
                
                cmd_say = ["say", "-v", macos_voice, "-r", str(wpm), "-o", str(temp_aiff), safe_text]
                res = subprocess.run(cmd_say, capture_output=True, text=True, timeout=15)
                
                # If Daniel isn't available, try generic Alex or system voice
                if res.returncode != 0:
                    cmd_say = ["say", "-v", "Alex", "-r", str(wpm), "-o", str(temp_aiff), safe_text]
                    res = subprocess.run(cmd_say, capture_output=True, text=True, timeout=15)

                if res.returncode == 0 and temp_aiff.exists():
                    cmd_ffmpeg = [
                        "ffmpeg", "-y",
                        "-i", str(temp_aiff),
                        "-af", "apad=pad_dur=0.25",
                        "-ar", "44100",
                        "-ac", "2",
                        str(out_wav)
                    ]
                    subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    if temp_aiff.exists():
                        temp_aiff.unlink()
                    
                    duration = self.get_audio_duration(out_wav)
                    self.last_measured_duration = duration
                    logger.info(f"[TTS] Synthesized macOS male voiceover for Scene {scene_idx}: {duration}s")
                    return out_wav, duration
            except Exception as e:
                logger.warning(f"[TTS] macOS say failed ({e}). Falling back to harmonic synthesis.")

        # 3. Last-resort fallback: Harmonic speech audio
        fallback_dur = target_duration or 4.0
        self._generate_harmonic_voice_wav(out_wav, fallback_dur, safe_text)
        self.last_measured_duration = fallback_dur
        return out_wav, fallback_dur

    def _generate_harmonic_voice_wav(self, out_path: Path, duration: float, text: str) -> Path:
        """Generate a soft, dynamic male voice-frequency audio waveform matching duration."""
        sample_rate = 44100
        total_samples = int(duration * sample_rate)
        base_freq = 135.0  # Male pitch register ~135 Hz
        
        with wave.open(str(out_path), "wb") as wav_file:
            wav_file.setnchannels(2)  # Stereo
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            frames = bytearray()
            for i in range(total_samples):
                t = i / sample_rate
                # Interactive speech envelope cadence
                cadence = 0.5 + 0.5 * math.sin(2 * math.pi * 3.2 * t)
                # Formants for masculine speech resonance (135Hz, 270Hz, 650Hz)
                val = (
                    0.45 * math.sin(2 * math.pi * base_freq * t) +
                    0.30 * math.sin(2 * math.pi * (base_freq * 2) * t) +
                    0.15 * math.sin(2 * math.pi * 650.0 * t)
                ) * cadence
                
                edge_envelope = min(1.0, t / 0.1, (duration - t) / 0.1) if duration > 0.2 else 1.0
                sample_val = int(val * edge_envelope * 14000.0)
                sample_val = max(-32767, min(32767, sample_val))
                frames.extend(struct.pack("<hh", sample_val, sample_val))
            
            wav_file.writeframes(frames)
            
        logger.info(f"[TTS] Generated harmonic speech audio: {out_path.name} ({duration}s)")
        return out_path

    def _generate_silence_wav(self, out_path: Path, duration: float) -> Path:
        """Generate silent audio track."""
        sample_rate = 44100
        total_samples = int(duration * sample_rate)
        with wave.open(str(out_path), "wb") as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(b"\x00\x00\x00\x00" * total_samples)
        return out_path

    def _trim_trailing_silence(self, wav_path: Path, pad_end_sec: float = 0.25) -> float:
        """Trims excessive trailing silence appended by neural TTS engines.
        
        Leaves a crisp pad_end_sec cushion so speech ends naturally and scene cuts
        transition instantaneously without dead lingering airtime.
        """
        try:
            with wave.open(str(wav_path), "rb") as wf:
                n_channels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                n_frames = wf.getnframes()
                data = wf.readframes(n_frames)

            samples = np.frombuffer(data, dtype=np.int16)
            mono = samples[::2] if n_channels == 2 else samples

            # 50ms energy evaluation windows
            win_size = int(0.05 * framerate)
            n_win = len(mono) // win_size
            if n_win == 0:
                return self.get_audio_duration(wav_path)

            energies = [np.max(np.abs(mono[i * win_size : (i + 1) * win_size])) for i in range(n_win)]
            active_idx = [i for i, e in enumerate(energies) if e > 500]

            if not active_idx:
                return self.get_audio_duration(wav_path)

            last_active_sample = (active_idx[-1] + 1) * win_size
            pad_samples = int(pad_end_sec * framerate)
            last_sample = min(len(mono), last_active_sample + pad_samples)

            trimmed_samples = samples[: last_sample * n_channels]
            with wave.open(str(wav_path), "wb") as wf:
                wf.setnchannels(n_channels)
                wf.setsampwidth(sampwidth)
                wf.setframerate(framerate)
                wf.writeframes(trimmed_samples.tobytes())

            new_dur = round(len(trimmed_samples) / (n_channels * framerate), 3)
            logger.info(f"[TTS] Trimmed trailing silence on {wav_path.name}: {n_frames/framerate:.2f}s -> {new_dur:.2f}s")
            return new_dur
        except Exception as e:
            logger.warning(f"[TTS] Could not trim trailing silence on {wav_path}: {e}")
            return self.get_audio_duration(wav_path)
