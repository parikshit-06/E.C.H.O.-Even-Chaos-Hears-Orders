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

    # default behavior
    print("[Echo Assistant] Available modes:")
    print("  python -m echo_assistant.main voice-demo   # continuous loop mode")
    print("  python -m echo_assistant.main hotkey       # press Ctrl+Space to talk")
    print()
    print("Current config:")
    print(config)

if __name__ == "__main__":
    main()
