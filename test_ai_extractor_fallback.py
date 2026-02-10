import unittest

from app.scraper.ai_extractor import AIExtractor


class _ExcWithStatus(Exception):
    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code


class AIExtractorFallbackTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extractor = AIExtractor.__new__(AIExtractor)
        cls.extractor.model_text = "gpt-4o-mini"
        cls.extractor.model_vision = "gpt-4o-mini"

    def setUp(self):
        self.extractor.fallback_model_text = "gpt-4.1-mini"
        self.extractor.fallback_model_vision = None

    def test_rate_limit_by_status_code_is_detected(self):
        self.assertTrue(
            self.extractor._is_rate_limit_error(
                _ExcWithStatus(429, "Too Many Requests")
            )
        )

    def test_rate_limit_by_message_is_detected(self):
        self.assertTrue(
            self.extractor._is_rate_limit_error(
                RuntimeError("rate_limit_exceeded: tokens per min")
            )
        )

    def test_non_rate_limit_error_is_not_detected(self):
        self.assertFalse(self.extractor._is_rate_limit_error(RuntimeError("timeout")))

    def test_fallback_model_is_resolved_for_text(self):
        self.assertEqual(
            self.extractor._resolve_fallback_model("gpt-4o-mini"),
            "gpt-4.1-mini",
        )

    def test_no_fallback_when_same_as_primary(self):
        self.extractor.fallback_model_text = "gpt-4o-mini"
        self.assertIsNone(self.extractor._resolve_fallback_model("gpt-4o-mini"))


if __name__ == "__main__":
    unittest.main()
