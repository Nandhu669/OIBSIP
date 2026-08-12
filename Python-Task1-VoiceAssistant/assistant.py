"""Command handling for the Beginner Voice Assistant task.

This module deliberately uses only the Python standard library so the command
behaviour can be tested without a microphone, browser, or text-to-speech engine.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable
from urllib.parse import quote_plus


@dataclass(frozen=True)
class CommandResult:
    """The outcome of processing one recognised voice command."""

    response: str
    should_exit: bool = False
    search_url: str | None = None


class VoiceAssistant:
    """Handles the required beginner commands and produces spoken responses."""

    def __init__(self, now: Callable[[], datetime] | None = None) -> None:
        self._now = now or datetime.now

    def handle_command(self, command: str) -> CommandResult:
        """Return the response and optional browser action for *command*."""
        normalized = command.strip().lower()

        if not normalized:
            return CommandResult("I did not catch that. Please say it again.")

        if "hello" in normalized or "hi" == normalized:
            return CommandResult("Hello! How can I help you today?")

        # Search must be checked before time/date. For example, "search for
        # time management" is a web search, not a request for the current time.
        topic = self._search_topic(normalized)
        if topic is not None:
            if not topic:
                return CommandResult("Please say what you would like me to search for.")
            return CommandResult(
                f"Searching the web for {topic}.",
                search_url=f"https://www.google.com/search?q={quote_plus(topic)}",
            )

        if "time" in normalized and "date" in normalized:
            current = self._now()
            return CommandResult(
                f"It is {current.strftime('%I:%M %p')} on {current.strftime('%A, %d %B %Y')}."
            )

        if "time" in normalized:
            return CommandResult(f"The time is {self._now().strftime('%I:%M %p')}.")

        if "date" in normalized or "day" in normalized:
            return CommandResult(f"Today is {self._now().strftime('%A, %d %B %Y')}.")

        if normalized in {"goodbye", "bye", "exit", "quit", "stop"}:
            return CommandResult("Goodbye! Have a great day.", should_exit=True)

        return CommandResult(
            "I can greet you, tell the time or date, or search the web. Please try again."
        )

    @staticmethod
    def _search_topic(command: str) -> str | None:
        """Extract a topic from supported search phrases, if a search was requested."""
        if command in {"search", "google", "look up"}:
            return ""
        for prefix in ("search for ", "search ", "google ", "look up "):
            if command.startswith(prefix):
                return command[len(prefix) :].strip()
        return None
