# Python Voice Assistant — OIBSIP Python Task 1

A microphone-based Python voice assistant built for the Oasis Infobyte Python Programming Internship (Task 1). It captures spoken commands from a microphone, converts speech to text, processes queries, speaks back responses using Text-to-Speech (TTS), and opens web browser searches on command.

---

## 📋 Requirements & Features Checklist

- [x] **Capture voice input using `speech_recognition` (microphone)** — Listens for audio via `speech_recognition.Microphone()` and transcribes speech using `recognize_google()`.
- [x] **Respond to "Hello" with a predefined greeting** — Greets the user with a friendly response when "hello" or "hi" is spoken.
- [x] **Tell the current time and date on request** — Dynamically computes and speaks the current time and date using Python's `datetime`.
- [x] **Perform a web search on a user-specified topic (open browser with query)** — Parses topics from phrases like "search for..." and automatically opens Google search in the default web browser.
- [x] **Graceful error handling: if voice is not understood, ask the user to repeat** — Catches unrecognized speech (`UnknownValueError`) and timeout errors cleanly without crashing, politely asking the user to repeat.
- [x] **Text-to-speech feedback using `pyttsx3` for all responses** — Delivers all assistant responses aloud through an offline `pyttsx3` engine.

---

## 🛠️ What We Used (Technologies & Libraries)

| Technology / Library | Purpose |
| :--- | :--- |
| **Python 3.10+** | Core programming language |
| **`speech_recognition`** (`SpeechRecognition==3.14.4`) | Captures microphone input and converts audio to text via Google Speech API |
| **`pyttsx3`** (`pyttsx3==2.99`) | Offline cross-platform Text-To-Speech (TTS) synthesis engine |
| **`PyAudio`** (`PyAudio==0.2.14`) | Low-level audio input stream binding required by SpeechRecognition for microphone access |
| **`webbrowser` & `os`** *(Standard Library)* | Opens web search results in the system's default browser (with Windows fallback) |
| **`datetime` & `urllib.parse`** *(Standard Library)* | Date/time formatting and URL parameter encoding |
| **`unittest`** *(Standard Library)* | Unit testing framework for testing command logic without requiring a physical microphone |

---

## ⚙️ How It Works

The Voice Assistant follows a clean, modular architecture split between hardware interface ([`main.py`](file:///c:/Users/nandh/.codex/.chatgpt-projects/g-p-6a781051c8988191b19dee4cc7bf18d5/OIBSIP/Python-Task1-VoiceAssistant/main.py)) and command processing logic ([`assistant.py`](file:///c:/Users/nandh/.codex/.chatgpt-projects/g-p-6a781051c8988191b19dee4cc7bf18d5/OIBSIP/Python-Task1-VoiceAssistant/assistant.py)):

```
[ User Microphone ] 
       │
       ▼
[ speech_recognition (Audio -> Text) ]
       │
       ▼
[ VoiceAssistant.handle_command() ] ──► (Matches: Hello | Time | Date | Web Search | Exit)
       │
       ├───────────────────────────────┐
       ▼                               ▼
[ pyttsx3 (Text-to-Speech Output) ]  [ Web Browser (Google Search) ]
```

1. **Initialization**: [`main.py`](file:///c:/Users/nandh/.codex/.chatgpt-projects/g-p-6a781051c8988191b19dee4cc7bf18d5/OIBSIP/Python-Task1-VoiceAssistant/main.py) initializes the `pyttsx3` speaker engine, `speech_recognition.Recognizer()`, and `speech_recognition.Microphone()`.
2. **Audio Capture**: Listens to the microphone with automatic ambient noise adjustment (`adjust_for_ambient_noise()`).
3. **Speech Recognition**: Transcribes captured speech into text using Google Speech Recognition API. If speech is unclear or silent, it catches exceptions gracefully and asks the user to repeat.
4. **Command Execution** ([`assistant.py`](file:///c:/Users/nandh/.codex/.chatgpt-projects/g-p-6a781051c8988191b19dee4cc7bf18d5/OIBSIP/Python-Task1-VoiceAssistant/assistant.py)):
   - **Greeting**: Matches "hello" or "hi" and returns a predefined greeting.
   - **Time & Date**: Checks for keywords "time", "date", or "day" and returns formatted local time/date.
   - **Web Search**: Identifies search prefixes ("search for", "google", "look up"), encodes the search topic into a Google search URL.
   - **Exit**: Matches exit commands ("goodbye", "exit", "quit", "stop") and terminates the loop cleanly.
5. **Speech Feedback & Actions**: Spoken response is synthesized out loud using `pyttsx3`. If a search URL was returned, [`open_search()`](file:///c:/Users/nandh/.codex/.chatgpt-projects/g-p-6a781051c8988191b19dee4cc7bf18d5/OIBSIP/Python-Task1-VoiceAssistant/main.py#L11-L32) launches the query in the default browser.

---

## 📁 Project Structure

```text
Python-Task1-VoiceAssistant/
├── assistant.py         # Pure command handling & logic (fully unit tested)
├── main.py              # Microphone listening, TTS output, browser launcher & main loop
├── requirements.txt     # Dependency specifications
├── README.md            # Documentation
└── tests/               # Unit tests
    ├── test_assistant.py# Command parsing & response tests
    └── test_main.py     # Speaker and browser helper tests
```

---

## 🚀 Setup & Execution

### 1. Prerequisites

- Python 3.10+
- A working microphone

### 2. Installation

Clone or download the project, create a virtual environment, and install dependencies:

```bash
# Create and activate virtual environment
python -m venv .venv

# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
```

### 3. Running the Assistant

```bash
python main.py
```

### 4. Running Tests

The core command logic can be verified without needing a microphone or external audio libraries:

```bash
python -m unittest discover tests
```

---

## 🗣️ Example Voice Commands

| Spoken Command | Action / Response |
| :--- | :--- |
| `"Hello"` | *"Hello! How can I help you today?"* |
| `"What is the time?"` | *"The time is 02:35 PM."* |
| `"What is today's date?"` | *"Today is Sunday, 09 August 2026."* |
| `"Search for Python voice assistant"` | Speaks *"Searching the web for Python voice assistant"* and opens Google Search in browser |
| `"Goodbye"` | *"Goodbye! Have a great day."* (Exits application) |
