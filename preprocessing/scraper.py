import os
import re

import requests
from bs4 import BeautifulSoup


class Scraper:
    BASE_URL = "http://www.songlyrics.com/index.php"
    ARTIST_ENDPOINT = (
        "?section=search&searchIn1=artist&searchW={artist_name}&pageNo={page_no}"
    )
    PAGE_THRESHOLD = 2

    @staticmethod
    def _extract_song_metadata(url: str) -> str:
        song_name = [part for part in url.split("/") if part][-1]
        return "_".join(song_name.split("-")[:-1])

    @staticmethod
    def _process_lyrics(lyrics: str) -> str:
        return re.sub(r"[^\w\s]", "", lyrics).lower()

    @staticmethod
    def _save_lyrics_to_file(
        path: str, song_name: str, artist_name: str, lyrics: str
    ) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
        artist_name = "_".join(artist_name.lower().split(" "))
        filename = song_name + "_" + artist_name + ".txt"
        with open(os.path.join(path, filename), "w") as f:
            f.write(lyrics)

    def scrape_lyrics(self, url: str):
        page = requests.get(url)
        song_name = self._extract_song_metadata(url)
        soup = BeautifulSoup(page.content, "html5lib")
        lyrics = soup.find("p", attrs={"id": "songLyricsDiv"})
        if lyrics is not None:
            return song_name, self._process_lyrics(lyrics.get_text())
        return "", ""

    def scrape_artist_lyrics(self, artist, output_dir: str = "data"):
        artist_name = "%20".join(artist.lower().split())
        for page in range(self.PAGE_THRESHOLD):
            endpoint = self.BASE_URL + self.ARTIST_ENDPOINT.format(
                artist_name=artist_name, page_no=page + 1
            )
            page = requests.get(endpoint)
            soup = BeautifulSoup(page.content, "html5lib")
            links = list(
                filter(
                    lambda x: "songlyrics.com" in x,
                    [
                        link.get("href")
                        for link in soup.find_all("a")
                        if link.get("href")
                    ],
                )
            )
            for link in links:
                song_name, lyrics = self.scrape_lyrics(link)
                if song_name and lyrics:
                    self._save_lyrics_to_file(output_dir, song_name, artist, lyrics)
