from unittest.mock import patch
import unittest

import main


class OpenSearchTests(unittest.TestCase):
    def test_returns_true_when_registered_browser_opens_url(self) -> None:
        with patch("main.webbrowser.open_new_tab", return_value=True):
            self.assertTrue(main.open_search("https://example.com"))

    def test_uses_windows_fallback_when_browser_is_not_registered(self) -> None:
        with patch("main.webbrowser.open_new_tab", return_value=False), patch(
            "main.sys.platform", "win32"
        ), patch("os.startfile", create=True) as startfile:
            self.assertTrue(main.open_search("https://example.com"))
            startfile.assert_called_once_with("https://example.com")


if __name__ == "__main__":
    unittest.main()
