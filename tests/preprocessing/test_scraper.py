from unittest import TestCase

from preprocessing.scraper import Scraper


class TestScraper(TestCase):
    def setUp(self) -> None:
        self.scraper = Scraper()

    def test_scrape_artist_lyrics(self):
        self.scraper.scrape_artist_lyrics("charlie puth")
