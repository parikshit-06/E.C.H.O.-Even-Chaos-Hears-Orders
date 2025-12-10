from .config import load_config


def main() -> None:
    import sys
    config = load_config()

    if len(sys.argv) > 1:
        mode = sys.argv[1]

        if mode == "voice-demo":
            from .runtime.loop import run_basic_voice_loop
            run_basic_voice_loop(config)
            return

        if mode == "hotkey":
            from .runtime.hotkey_listener import run_hotkey_listener
            run_hotkey_listener(config)
            return

        if mode == "wake":
            from .runtime.wake_listener import run_wake_listener
            run_wake_listener(config)
            return

    print("[Echo Assistant] Available modes:")
    print("  python -m echo_assistant.main voice-demo   # continuous 4s loop")
    print("  python -m echo_assistant.main hotkey       # Ctrl+Space to talk")
    print("  python -m echo_assistant.main wake         # wake-word (Porcupine) mode")
    print()
    print("Current config:")
    print(config)


if __name__ == "__main__":
    main()
