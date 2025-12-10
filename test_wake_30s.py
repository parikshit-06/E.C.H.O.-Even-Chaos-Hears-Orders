#!/usr/bin/env python
"""Test wake-word detection with output to file"""
import sys
sys.path.insert(0, 'src')

from echo_assistant.config import load_config
from echo_assistant.core.wakeword import WakeWordConfig, WakeWordDetector

if __name__ == "__main__":
    config = load_config()
    print("[Test] Starting wake-word detection test...")
    print("[Test] Speak 'hey Jarvis' clearly near your microphone now!")
    print("[Test] Running for 30 seconds...")
    
    ww_cfg = WakeWordConfig(
        model_names=["hey jarvis"],
        threshold=0.1,
        smoothing_window=5,
    )
    detector = WakeWordDetector(ww_cfg)
    
    detection_count = 0
    
    def on_wake():
        global detection_count
        detection_count += 1
        print(f"\n✅ WAKE #{detection_count} DETECTED!\n")
    
    import threading
    import time
    
    # Run detector in thread so we can timeout
    detector_thread = threading.Thread(target=lambda: detector.run(on_detect=on_wake), daemon=True)
    detector_thread.start()
    
    try:
        time.sleep(30)  # Run for 30 seconds
    except KeyboardInterrupt:
        pass
    
    print(f"\n[Test] Stopped. Total detections: {detection_count}")
