"""System tray icon and menu for background service."""

import logging
import threading
from typing import Callable, Optional

try:
    import pystray
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("[Tray] pystray not installed. Run: pip install pystray pillow")

logger = logging.getLogger(__name__)


class TrayIcon:
    """System tray icon for E.C.H.O Assistant."""
    
    def __init__(
        self,
        on_exit: Optional[Callable] = None,
        icon_path: Optional[str] = None,
        icon_path_on: Optional[str] = None,
        icon_path_off: Optional[str] = None,
    ):
        """Initialize the tray icon.

        icon_path:      Single custom icon for both states.
        icon_path_on:   Icon when listening (overrides icon_path for on state).
        icon_path_off:  Icon when paused (overrides icon_path for off state).
        """
        self.on_exit = on_exit
        self.icon = None
        self.is_listening = True
        self.custom_image_on = None
        self.custom_image_off = None
        
        if not TRAY_AVAILABLE:
            logger.warning("Tray icon not available - pystray not installed")
            return
            
        # Resolve which paths to use
        on_path = icon_path_on or icon_path
        off_path = icon_path_off or icon_path_on or icon_path

        # Load custom icons if provided; fall back to generated icon
        if on_path:
            self.custom_image_on = self._load_custom_icon(on_path)
            if self.custom_image_on:
                logger.info("Tray icon (on) initialized with custom image")
        if off_path:
            self.custom_image_off = self._load_custom_icon(off_path)
            if self.custom_image_off:
                logger.info("Tray icon (off) initialized with custom image")
        
        # Start with listening icon (on)
        self.image = self.custom_image_on or self._create_icon_image("green")
        logger.info("Tray icon initialized")

    def _load_custom_icon(self, icon_path: str):
        """Load and resize a user-provided icon to 64x64."""
        try:
            img = Image.open(icon_path).convert("RGBA")
            img = img.resize((64, 64), Image.LANCZOS)
            return img
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(f"Failed to load custom tray icon '{icon_path}': {exc}")
            return None
    
    def _create_icon_image(self, color="green"):
        """Create a simple colored circle icon."""
        # Create a 64x64 image
        image = Image.new('RGB', (64, 64), color='white')
        draw = ImageDraw.Draw(image)
        
        # Draw a circle
        if color == "green":
            fill = (34, 139, 34)  # Forest green
        elif color == "red":
            fill = (220, 20, 60)  # Crimson
        else:
            fill = (70, 130, 180)  # Steel blue
            
        draw.ellipse([8, 8, 56, 56], fill=fill, outline='black', width=2)
        
        # Add "E" letter in the center
        draw.text((24, 20), "E", fill='white')
        
        return image
    
    def _toggle_listening(self, icon, item):
        """Toggle listening state."""
        self.is_listening = not self.is_listening
        status = "Listening" if self.is_listening else "Paused"
        logger.info(f"Tray: Toggled to {status}")
        # Update icon according to state
        if self.is_listening and self.custom_image_on:
            icon.icon = self.custom_image_on
        elif (not self.is_listening) and self.custom_image_off:
            icon.icon = self.custom_image_off
        else:
            color = "green" if self.is_listening else "red"
            icon.icon = self._create_icon_image(color)
    
    def _exit_app(self, icon, item):
        """Exit the application."""
        logger.info("Tray: Exit requested")
        icon.stop()
        if self.on_exit:
            self.on_exit()
    
    def create_menu(self):
        """Create the tray menu."""
        if not TRAY_AVAILABLE:
            return None
            
        return pystray.Menu(
            pystray.MenuItem(
                lambda text: f"{'🟢 Listening' if self.is_listening else '🔴 Paused'}",
                self._toggle_listening,
                default=True
            ),
            pystray.MenuItem('Exit E.C.H.O.', self._exit_app)
        )
    
    def run(self):
        """Show the tray icon and run (blocking)."""
        if not TRAY_AVAILABLE:
            logger.warning("Cannot show tray - pystray not available")
            return
            
        self.icon = pystray.Icon(
            "E.C.H.O. Assistant",
            self.image,
            "E.C.H.O. Assistant - Listening",
            self.create_menu()
        )
        
        logger.info("Starting system tray icon")
        self.icon.run()
    
    def run_detached(self):
        """Run tray icon in a separate thread."""
        if not TRAY_AVAILABLE:
            return
            
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        logger.info("Tray icon running in background thread")
    
    def stop(self):
        """Stop the tray icon."""
        if self.icon:
            self.icon.stop()
            logger.info("Tray icon stopped")
