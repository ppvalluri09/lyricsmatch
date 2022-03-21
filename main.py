import argparse

from engine.posting import PostingListProcessor
from engine.search import LyricsSearch
from preprocessing.scraper import Scraper
from preprocessing.vocab import Vocabulary

vocab = Vocabulary("data")
posting_list_processor = PostingListProcessor(vocab)
search_engine = LyricsSearch(vocab, posting_list_processor)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--artist",
    action="store",
    type=str,
    required=False,
    help="Name of the artist who's song lyrics have to be scraped",
)
parser.add_argument(
    "--output",
    action="store",
    type=str,
    required=False,
    help="Output directory to which the scraped lyrics are to be saved",
)
parser.add_argument(
    "--query",
    action="store",
    type=str,
    required=False,
    help="Input query that has to be searched",
)

args = parser.parse_args()

if args.artist:
    scraper = Scraper()
    scraper.scrape_artist_lyrics(args.artist, args.output)
elif args.query:
    search_engine.search(args.query)

# if __name__ == "__main__":
#     search_engine.search("smooth or like or butter")
