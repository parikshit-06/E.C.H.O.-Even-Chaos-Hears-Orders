"""
wakeword.py
openWakeWord-based wake-word detection for Echo.

Uses pre-trained models like "hey jarvis", "alexa", etc.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional

import numpy as np
import sounddevice as sd
import openwakeword
from openwakeword.model import Model


@dataclass
class WakeWordConfig:
    # Names of pre-trained wakeword models, e.g. ["hey jarvis"]
    # If empty, openWakeWord will load all available models.
    model_names: Optional[List[str]] = None
    threshold: float = 0.5  # score threshold for activation (0–1)
    smoothing_window: int = 5  # number of frames to average for smoothing


class WakeWordDetector:
    def __init__(self, config: WakeWordConfig) -> None:
        # Store the original model names that user provided
        # These will be simple names like "hey jarvis"
        # CRITICAL: Save this BEFORE creating Model(), and pass a COPY to Model()
        # because Model() modifies the list in-place to full file paths
        self.target_model_names = config.model_names.copy() if config.model_names else None
        self.config = config

        # One-time download of pre-trained models (no account needed)
        openwakeword.utils.download_models()

        # Load specified models, or all if None
        # Pass a COPY so Model() doesn't modify our target_model_names
        models_to_load = self.target_model_names.copy() if self.target_model_names else None
        self.model = Model(
            wakeword_models=models_to_load,
            # you can add vad_threshold here later if needed
        )

        # openWakeWord expects 16 kHz, 16-bit mono PCM
        self.sample_rate = 16_000
        # Use 80 ms frames -> 1280 samples
        self.frame_length = int(self.sample_rate * 0.08)
        
        # Score smoothing: keep a rolling window of scores per model
        # The prediction dict uses model names like "hey jarvis", not file paths
        self.score_history = {}

        print(
            f"[WakeWord] Using openWakeWord models: "
            f"{self.target_model_names or 'ALL'}; threshold={self.config.threshold}"
        )
    
    def _smooth_score(self, name: str, score: float) -> float:
        """
        Apply rolling average smoothing to stabilize detection.
        """
        if name not in self.score_history:
            self.score_history[name] = []
        
        self.score_history[name].append(float(score))
        
        # Keep only the last N frames
        if len(self.score_history[name]) > self.config.smoothing_window:
            self.score_history[name].pop(0)
        
        # Return average of the window
        avg_score = np.mean(self.score_history[name])
        
        # Also return max of recent frames (for peak detection)
        return avg_score
    
    def _should_trigger(self, name: str, smoothed_score: float) -> bool:
        """
        Determine if we should trigger detection.
        Trigger if smoothed score is high enough, OR if we have a recent peak.
        """
        if name not in self.score_history:
            return False
        
        # Get the last few raw scores
        recent_scores = self.score_history[name][-3:] if len(self.score_history[name]) >= 3 else self.score_history[name]
        max_recent = max(recent_scores) if recent_scores else 0
        
        # Trigger if:
        # 1. Smoothed score is above threshold, OR
        # 2. Any of the last 3 frames exceeded threshold * 2.5 (peak detection)
        cond1 = smoothed_score >= self.config.threshold
        cond2 = max_recent >= (self.config.threshold * 2.5)
        
        # Debug: log every evaluation for this model
        if max_recent > 0.05:  # Only log when there's actually a signal
            print(f"[WakeWord DEBUG] {name}: smoothed={smoothed_score:.4f}, max_recent={max_recent:.4f}, "
                  f"threshold={self.config.threshold}, peak_thresh={self.config.threshold * 2.5:.4f}, "
                  f"cond1(smooth)={cond1}, cond2(peak)={cond2}, TRIGGER={cond1 or cond2}")
        
        return cond1 or cond2

    def run(self, on_detect: Callable[[], None]) -> None:
        """
        Blocking loop: listens on mic and calls on_detect()
        whenever a wakeword score passes the threshold.
        """
        print(
            f"[WakeWord] Listening at {self.sample_rate} Hz, "
            f"frame_length={self.frame_length} samples."
        )
        model_display = self.config.model_names[0] if self.config.model_names else "any"
        # Extract just the model name if it's a file path
        if "/" in model_display or "\\" in model_display:
            model_display = model_display.split("/")[-1].split("\\")[-1].replace("_v0.1.tflite", "")
        print(f"[WakeWord] Waiting for wake word: '{model_display}'...")

        frame_count = 0
        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.frame_length,
                dtype="int16",
                channels=1,
            ) as audio_stream:
                while True:
                    frame, _ = audio_stream.read(self.frame_length)
                    if not frame:
                        continue

                    # int16 PCM -> numpy
                    audio = np.frombuffer(frame, dtype=np.int16)

                    # prediction is a dict: {"hey jarvis": score, ...}
                    preds = self.model.predict(audio)

                    # Apply smoothing to each score
                    smoothed_preds = {}
                    for name, score in preds.items():
                        smoothed_preds[name] = self._smooth_score(name, score)

                    # Debug output every 10 frames (80ms * 10 = 800ms)
                    frame_count += 1
                    if frame_count % 10 == 0:
                        print(f"[WakeWord] Raw scores: {preds}")
                        print(f"[WakeWord] Smoothed: {smoothed_preds}")

                    # Check if any chosen model passes smoothed threshold
                    for name, smoothed_score in smoothed_preds.items():
                        should_trigger = self._should_trigger(name, smoothed_score)
                        
                        # Check if this model name should be accepted
                        # The 'name' from predictions will be like "hey jarvis" (the model key)
                        # Use target_model_names for comparison (our saved copy)
                        if self.target_model_names:
                            # If specific models configured, only trigger on those
                            is_in_models = name in self.target_model_names
                        else:
                            # If no specific models configured, accept any
                            is_in_models = True
                        
                        # Debug: show trigger status
                        if should_trigger:
                            if name in self.score_history and self.score_history[name]:
                                max_recent = max(self.score_history[name][-3:]) if len(self.score_history[name]) >= 3 else 0
                                print(f"[WakeWord] ⚠️  TRIGGER: '{name}', max={max_recent:.3f}, in_models={is_in_models}, targets={self.target_model_names}")
                        
                        if should_trigger and is_in_models:
                            print(f"[WakeWord] ✅ DETECTED '{name}' with smoothed score {smoothed_score:.3f}")
                            on_detect()
                            # After a wake, clear the history to avoid re-triggering
                            self.score_history[name] = []
                            # After a wake, don't immediately re-trigger on same audio
                            break
        except Exception as e:
            print(f"[WakeWord] Error in detection loop: {e}")
            raise
