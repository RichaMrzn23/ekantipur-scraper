"""Central settings for the scraper (timeouts, URLs, browser flags)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ScraperConfig:
    base_url: str = "https://ekantipur.com"
    headless: bool = False
    default_timeout_ms: int = 30_000
    viewport_width: int = 1280
    viewport_height: int = 720
