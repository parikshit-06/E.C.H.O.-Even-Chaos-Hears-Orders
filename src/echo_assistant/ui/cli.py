"""Simple CLI status output for E.C.H.O Assistant."""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CLI:
    """Command-line interface for status and interaction."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.start_time = datetime.now()
        logger.info("CLI initialized")
    
    def print_status(self, message, status_type="INFO"):
        """Print a status message."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ",
            "SUCCESS": "✓",
            "ERROR": "✗",
            "LISTENING": "🎤",
            "SPEAKING": "🔊",
        }.get(status_type, "•")
        
        print(f"[{timestamp}] {prefix} {message}")
    
    def print_banner(self):
        """Print the startup banner."""
        banner = """
        ╔════════════════════════════════════════╗
        ║     E.C.H.O Assistant v0.1.0          ║
        ║  Enhanced Conversational Helper OS     ║
        ╚════════════════════════════════════════╝
        """
        print(banner)
    
    def print_help(self):
        """Print help information."""
        help_text = """
        Available Commands:
        - "open [app]" - Open an application
        - "search [query]" - Search the web
        - "note [content]" - Take a quick note
        - "volume [up/down/mute]" - Control volume
        - Or just talk naturally for a conversation!
        
        Press Ctrl+C to exit.
        """
        print(help_text)
    
    def print_uptime(self):
        """Print the uptime."""
        uptime = datetime.now() - self.start_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}")
