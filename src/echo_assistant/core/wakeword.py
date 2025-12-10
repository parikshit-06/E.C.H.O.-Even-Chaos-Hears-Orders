"""Wake-word detection and hotkey abstraction (future implementation)."""

import logging

logger = logging.getLogger(__name__)


class WakeWordDetector:
    """Handles wake-word detection."""
    
    def __init__(self, wake_word="echo"):
        """Initialize wake-word detector."""
        self.wake_word = wake_word.lower()
        logger.info(f"Wake-word detector initialized: {wake_word}")
    
    def detect(self, audio_data):
        """Detect wake-word in audio data."""
        # TODO: Implement actual wake-word detection
        # This is a placeholder for future implementation
        logger.warning("Wake-word detection not yet implemented")
        return False
    
    def is_active(self):
        """Check if wake-word detection is active."""
        return False  # Not implemented yet
