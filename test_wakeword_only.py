#!/usr/bin/env python
"""Test wake-word detection directly - skip TTS for now"""
import sys
sys.path.insert(0, 'src')

from echo_assistant.config import load_config
from echo_assistant.core.wakeword import WakeWordConfig, WakeWordDetector

if __name__ == "__main__":
    config = load_config()
    print("[Test] Starting wake-word detection test...")
    print("[Test] Try saying 'hey Jarvis' 2-3 times near your microphone...")
    
    ww_cfg = WakeWordConfig(
        model_names=["hey jarvis"],
        threshold=0.1,  # Lower threshold - peak detection helps
        smoothing_window=5,
    )
    detector = WakeWordDetector(ww_cfg)
    
    detection_count = 0
    
    def on_wake():
        global detection_count
        detection_count += 1
        print(f"\n✅ WAKE #{detection_count} DETECTED!\n")
    
    try:
        detector.run(on_detect=on_wake)
    except KeyboardInterrupt:
        print(f"\n[Test] Stopped. Total detections: {detection_count}")
    except Exception as e:
        print(f"[Test] Error: {e}")
        import traceback
        traceback.print_exc()
