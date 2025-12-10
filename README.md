# E.C.H.O. Assistant
## Even Chaos Hears Orders

A powerful, modular voice-activated AI assistant built with Python. E.C.H.O. provides hands-free interaction through wake-word detection or hotkey activation, combining local speech recognition with advanced AI language models.

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎤 Voice Interaction
- **Wake-word detection** using openWakeWord ("hey Jarvis")
- **Hotkey activation** (Ctrl+Space) for instant interaction
- **Local speech-to-text** with Faster Whisper (offline capable)
- **Text-to-speech** with pyttsx3 (cross-platform)

### 🤖 AI Intelligence
- **Multiple LLM backends**:
  - Perplexity AI (default) - Real-time web-connected reasoning
  - Google Gemini - Advanced multimodal AI
- **Conversational context** - Remembers conversation flow
- **Smart routing** - Delegates tasks to specialized skills

### 🛠️ Skills & Capabilities
- **Web search** - Real-time information lookup
- **Note-taking** - Create and manage notes via voice
- **Media control** - Play music and videos
- **System control** - Control PC functions (volume, shutdown, etc.)
- **Memory** - Persistent conversation history
- **Extensible architecture** - Easy to add custom skills

### 🎨 User Interface
- **CLI mode** - Simple command-line interface
- **System tray** - Background operation with tray icon
- **Multiple interaction modes** - Hotkey or wake-word

## 📋 Requirements

- Python 3.8 or higher
- Microphone for voice input
- Internet connection (for LLM backends)
- Windows, macOS, or Linux

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/parikshit-06/E.C.H.O.-Even-Chaos-Hears-Orders.git
cd E.C.H.O
```

### 2. Install Dependencies
```bash
pip install -e .
```

**Additional dependencies:**
```bash
pip install faster-whisper sounddevice openwakeword requests google-generativeai numpy
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# LLM Backend Selection
LLM_BACKEND=perplexity  # or 'gemini'

# Perplexity API (https://www.perplexity.ai/)
PERPLEXITY_API_KEY=your_perplexity_api_key_here
PERPLEXITY_MODEL=sonar-reasoning

# Google Gemini API (https://aistudio.google.com/apikey)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=models/gemini-2.5-pro

# Wake-word Configuration (optional)
WAKEWORD_KEYWORD=hey jarvis
```

### 4. Run the Assistant

**Wake-word mode** (always listening):
```bash
python -m echo_assistant.main wake
```

**Hotkey mode** (press Ctrl+Space):
```bash
python -m echo_assistant.main hotkey
```

**CLI mode** (type to interact):
```bash
python -m echo_assistant.main cli
```

## 📁 Project Structure

```
E.C.H.O/
├── src/
│   └── echo_assistant/
│       ├── core/               # Core engine components
│       │   ├── audio.py        # Audio recording/playback
│       │   ├── stt.py          # Speech-to-text (Whisper)
│       │   ├── tts.py          # Text-to-speech (pyttsx3)
│       │   ├── brain.py        # LLM integration (Perplexity/Gemini)
│       │   ├── router.py       # Intent routing & skill dispatch
│       │   └── wakeword.py     # Wake-word detection (openWakeWord)
│       │
│       ├── runtime/            # Orchestration & event loops
│       │   ├── loop.py         # Main interaction loop
│       │   ├── service.py      # Background service manager
│       │   ├── wake_listener.py    # Wake-word listener
│       │   └── hotkey_listener.py  # Hotkey listener
│       │
│       ├── skills/             # Capability modules
│       │   ├── web_search.py   # Web search integration
│       │   ├── notes.py        # Note-taking functionality
│       │   ├── media.py        # Media playback control
│       │   ├── system_control.py   # System commands
│       │   └── memory.py       # Conversation history
│       │
│       ├── ui/                 # User interfaces
│       │   ├── cli.py          # Command-line interface
│       │   └── tray.py         # System tray icon
│       │
│       ├── config.py           # Configuration management
│       ├── logging_config.py   # Logging setup
│       └── main.py             # Entry point
│
├── pyproject.toml              # Project metadata & dependencies
├── .env                        # Environment variables (create this)
└── README.md                   # This file
```

## 🔧 Configuration

### Audio Settings

Edit `src/echo_assistant/config.py`:

```python
sample_rate: int = 16_000       # Audio sample rate (Hz)
audio_channels: int = 1         # Mono audio
stt_model_name: str = "small"   # Whisper model: tiny/base/small/medium/large
stt_device: str = "cpu"         # Device: cpu/cuda
```

### Wake-word Settings

```python
wakeword_keyword: str = "hey jarvis"  # Available: "hey jarvis", "alexa", "ok google"
hotkey: str = "ctrl+space"            # Hotkey combination
```

### LLM Settings

Switch between backends in `.env`:
```env
LLM_BACKEND=perplexity  # or 'gemini'
```

## 🎯 Usage Examples

### Voice Commands

**Information queries:**
- "Hey Jarvis, what's the weather today?"
- "Hey Jarvis, tell me about quantum computing"
- "Hey Jarvis, search for the latest news on AI"

**Note-taking:**
- "Hey Jarvis, take a note: Buy groceries tomorrow"
- "Hey Jarvis, show my notes"

**Media control:**
- "Hey Jarvis, play some jazz music"
- "Hey Jarvis, pause the music"

**System control:**
- "Hey Jarvis, increase volume"
- "Hey Jarvis, lock my computer"

## 🧪 Testing

Test individual components:

```bash
# Test wake-word detection only
python test_wakeword_only.py

# Test full wake-word with voice response
python test_wake_30s.py

# Test Gemini API connection
python debug_gemini_models.py
```

## 🛠️ Development

### Adding Custom Skills

Create a new skill in `src/echo_assistant/skills/`:

```python
# my_skill.py
def handle_my_skill(user_input: str) -> str:
    """
    Custom skill handler.
    
    Args:
        user_input: User's voice command
        
    Returns:
        Response text to be spoken
    """
    # Your logic here
    return "Skill executed successfully"
```

Register in `router.py`:
```python
from echo_assistant.skills.my_skill import handle_my_skill

# Add routing logic
if "trigger phrase" in user_input.lower():
    return handle_my_skill(user_input)
```

### Code Style

The project uses standard Python conventions:
- Type hints for better code clarity
- Docstrings for all public functions
- Modular architecture for easy maintenance

## 📝 API Keys

### Get Perplexity API Key
1. Visit [Perplexity AI](https://www.perplexity.ai/)
2. Sign up for an account
3. Navigate to API settings
4. Generate an API key

### Get Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with Google account
3. Create a new API key
4. Copy to your `.env` file

## 🐛 Troubleshooting

### Wake-word not detecting

- Ensure microphone is working and properly configured
- Try speaking louder or closer to microphone
- Check that `openwakeword` models are downloaded (automatic on first run)
- Verify audio permissions are granted

### STT not working

- Check that `faster-whisper` is installed correctly
- Verify microphone access permissions
- Try a smaller model (`tiny` or `base`) for faster processing
- Ensure sufficient disk space for model downloads

### API errors

- Verify API keys are correct in `.env`
- Check internet connection
- Ensure API key has sufficient credits/quota
- Review rate limits for your API tier

### Audio device errors

- List available audio devices:
```python
import sounddevice as sd
print(sd.query_devices())
```
- Specify device index in `audio.py` if needed

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for:

- Bug fixes
- New skills/features
- Documentation improvements
- Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **openWakeWord** - Wake-word detection
- **Faster Whisper** - Speech-to-text engine
- **pyttsx3** - Text-to-speech engine
- **Perplexity AI** - Real-time reasoning LLM
- **Google Gemini** - Advanced multimodal AI

## 📧 Contact

**Author:** Parikshit  
**GitHub:** [@parikshit-06](https://github.com/parikshit-06)  
**Repository:** [E.C.H.O.-Even-Chaos-Hears-Orders](https://github.com/parikshit-06/E.C.H.O.-Even-Chaos-Hears-Orders)

---

**E.C.H.O.** - *Your voice, your command, your AI assistant.*
