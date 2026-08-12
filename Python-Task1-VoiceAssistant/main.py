"""Microphone and text-to-speech interface for the Beginner Voice Assistant."""

from __future__ import annotations

import sys
import webbrowser

from assistant import VoiceAssistant


def open_search(url: str) -> bool:
    """Open *url* in the default browser, with a Windows fallback.

    ``webbrowser`` can fail silently when no browser is registered, so its
    Boolean result is checked and Windows' URL launcher is tried as a fallback.
    """
    try:
        if webbrowser.open_new_tab(url):
            return True
    except webbrowser.Error as error:
        print(f"Browser launcher error: {error}")

    if sys.platform.startswith("win"):
        try:
            import os

            os.startfile(url)  # type: ignore[attr-defined]  # Windows-only API
            return True
        except OSError as error:
            print(f"Windows could not open the browser: {error}")

    return False


def create_speaker():
    """Create a pyttsx3 speaker and give an actionable error if setup is incomplete."""
    try:
        import pyttsx3
    except ImportError as error:
        raise RuntimeError("pyttsx3 is not installed. Run: pip install -r requirements.txt") from error

    try:
        engine = pyttsx3.init()
    except Exception as error:  # pyttsx3 exposes platform-specific backend errors.
        raise RuntimeError(f"Could not start text-to-speech: {error}") from error

    engine.setProperty("rate", 175)

    def speak(message: str) -> None:
        print(f"Assistant: {message}")
        engine.say(message)
        engine.runAndWait()

    return speak


def listen(recognizer, microphone) -> str | None:
    """Listen once and return recognised speech, or None when it was not understood."""
    import speech_recognition as sr

    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        command = recognizer.recognize_google(audio)
        print(f"You: {command}")
        return command
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as error:
        print(f"Speech recognition service error: {error}")
        return None
    except OSError as error:
        print(f"Microphone error: {error}")
        return None


def main() -> int:
    try:
        import speech_recognition as sr
    except ImportError:
        print("speech_recognition is not installed. Run: pip install -r requirements.txt")
        return 1

    try:
        speak = create_speaker()
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
    except RuntimeError as error:
        print(error)
        return 1
    except OSError as error:
        print(f"Could not access a microphone: {error}")
        return 1

    assistant = VoiceAssistant()
    speak("Voice Assistant is ready. Say hello, ask for the time or date, or say search for followed by a topic.")

    while True:
        command = listen(recognizer, microphone)
        if command is None:
            speak("I did not understand that. Please repeat.")
            continue

        result = assistant.handle_command(command)
        speak(result.response)
        if result.search_url:
            if not open_search(result.search_url):
                speak("I could not open your browser. Please set a default browser and try again.")
        if result.should_exit:
            return 0


if __name__ == "__main__":
    sys.exit(main())
