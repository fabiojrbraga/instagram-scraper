import unittest

from app.scraper.instagram_scraper import InstagramScraper


class RecentPostTimeParsingTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Avoid heavy client initialization; these helpers are pure methods.
        cls.scraper = InstagramScraper.__new__(InstagramScraper)

    def test_relative_minutes_plural_is_parsed(self):
        hours = self.scraper._relative_time_to_hours("44 minutes ago")
        self.assertIsNotNone(hours)
        self.assertAlmostEqual(hours, 44 / 60, places=4)

    def test_relative_minutes_singular_is_parsed(self):
        hours = self.scraper._relative_time_to_hours("1 minute ago")
        self.assertIsNotNone(hours)
        self.assertAlmostEqual(hours, 1 / 60, places=4)

    def test_recent_post_within_window_for_recent_days(self):
        self.assertTrue(self.scraper._is_recent_post("44 minutes ago", recent_days=3))

    def test_post_outside_window(self):
        self.assertFalse(self.scraper._is_recent_post("4 days ago", recent_days=3))


if __name__ == "__main__":
    unittest.main()
