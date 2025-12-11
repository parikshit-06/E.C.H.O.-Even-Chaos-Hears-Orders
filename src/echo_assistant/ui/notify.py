"""Styled notification helper for showing modern popup overlays."""

import threading
import tkinter as tk
from tkinter import scrolledtext


def _create_styled_popup(title: str, message: str):
    """Create and show a modern dark-themed popup window with scrollable text."""
    root = tk.Tk()
    root.title("E.C.H.O. Assistant")
    
    # Window properties
    root.attributes("-topmost", True)
    root.resizable(True, True)
    
    # Larger default size
    width = 600
    height = 400
    
    # Center on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Dark theme colors
    bg_color = "#1e1e1e"  # Dark background
    fg_color = "#e0e0e0"  # Light text
    header_color = "#1C2534"  # Deep blue header
    header_text = "#ffffff"
    
    root.configure(bg=bg_color)
    
    # Title bar
    title_frame = tk.Frame(root, bg=header_color, height=60)
    title_frame.pack(fill=tk.X, padx=0, pady=0)
    title_frame.pack_propagate(False)
    
    title_label = tk.Label(
        title_frame,
        text="🎤 " + title,
        font=("Segoe UI", 14, "bold"),
        bg=header_color,
        fg=header_text
    )
    title_label.pack(pady=15)
    
    # Scrollable text area with frame
    text_frame = tk.Frame(root, bg=bg_color)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    # Use ScrolledText for automatic scrollbars
    text_widget = scrolledtext.ScrolledText(
        text_frame,
        font=("Segoe UI", 11),
        bg="#2d2d2d",  # Slightly lighter than main bg for contrast
        fg=fg_color,
        relief=tk.FLAT,
        borderwidth=1,
        wrap=tk.WORD,
        height=12,
        width=65,
        insertbackground=fg_color,
        selectbackground="#0d47a1",
        selectforeground=header_text
    )
    text_widget.pack(fill=tk.BOTH, expand=True)
    text_widget.insert(tk.END, message)
    text_widget.config(state=tk.DISABLED)  # Read-only
    
    # Button frame
    btn_frame = tk.Frame(root, bg=bg_color)
    btn_frame.pack(fill=tk.X, padx=20, pady=15)
    
    ok_btn = tk.Button(
        btn_frame,
        text="Close",
        font=("Segoe UI", 10, "bold"),
        bg=header_color,
        fg=header_text,
        command=root.quit,
        activebackground="#1565c0",
        activeforeground=header_text,
        relief=tk.FLAT,
        padx=30,
        pady=10,
        cursor="hand2",
        bd=0
    )
    ok_btn.pack(side=tk.RIGHT)
    
    try:
        root.mainloop()
    except:
        pass
    finally:
        try:
            root.destroy()
        except:
            pass


def show_popup(title: str, message: str):
    """Show a styled popup overlay in a non-blocking thread."""
    def _show():
        try:
            _create_styled_popup(title, message)
        except Exception as e:
            # Fallback: print to console if GUI fails
            print(f"[{title}] {message}")

    threading.Thread(target=_show, daemon=True).start()
