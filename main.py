"""Entry point: configure Playwright, run scrapers, write output."""

import json
from pathlib import Path

from browser import page_session
from config import ScraperConfig
from scrapers.ekantipur import EkantipurScraper


def main() -> None:
    config = ScraperConfig()
    output_path = Path(__file__).resolve().parent / "output.json"

    with page_session(config) as page:
        scraper = EkantipurScraper(page)
        entertainment = scraper.scrape_entertainment(config.base_url)
        cartoon = scraper.scrape_cartoon()

    output = {
        "entertainment_news": entertainment,
        "cartoon_of_the_day": cartoon,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
