from datetime import datetime
import unittest

from assistant import VoiceAssistant


class VoiceAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assistant = VoiceAssistant(lambda: datetime(2026, 8, 9, 14, 35))

    def test_hello_gets_a_greeting(self) -> None:
        self.assertIn("Hello", self.assistant.handle_command("hello").response)

    def test_time_and_date_are_reported(self) -> None:
        response = self.assistant.handle_command("tell me the time and date").response
        self.assertIn("02:35 PM", response)
        self.assertIn("Sunday, 09 August 2026", response)

    def test_search_builds_a_safe_google_url(self) -> None:
        result = self.assistant.handle_command("search for Python voice assistant")
        self.assertEqual(
            result.search_url,
            "https://www.google.com/search?q=python+voice+assistant",
        )

    def test_search_phrase_with_time_is_not_misclassified(self) -> None:
        result = self.assistant.handle_command("search for time management")
        self.assertEqual(result.search_url, "https://www.google.com/search?q=time+management")

    def test_empty_search_asks_for_a_topic(self) -> None:
        result = self.assistant.handle_command("search")
        self.assertIsNone(result.search_url)
        self.assertIn("what you would like", result.response)

    def test_unknown_speech_has_a_helpful_response(self) -> None:
        self.assertIn("Please try again", self.assistant.handle_command("play music").response)

    def test_goodbye_exits(self) -> None:
        self.assertTrue(self.assistant.handle_command("goodbye").should_exit)


if __name__ == "__main__":
    unittest.main()
