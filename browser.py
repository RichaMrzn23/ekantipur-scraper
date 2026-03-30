"""Playwright lifecycle: browser launch, page defaults, clean shutdown."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from playwright.sync_api import Browser, Page, Playwright, sync_playwright

from config import ScraperConfig


def _apply_page_defaults(page: Page, config: ScraperConfig) -> None:
    page.set_default_timeout(config.default_timeout_ms)
    page.set_viewport_size(
        {"width": config.viewport_width, "height": config.viewport_height}
    )


@contextmanager
def browser_session(
    config: ScraperConfig | None = None,
) -> Generator[tuple[Playwright, Browser, Page], None, None]:
    """
    Yields (playwright, browser, page). Closes browser when the block exits.

    Use when you need access to `playwright` or `browser` (e.g. multiple contexts).
    """
    cfg = config or ScraperConfig()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=cfg.headless)
        page = browser.new_page()
        _apply_page_defaults(page, cfg)
        try:
            yield p, browser, page
        finally:
            browser.close()


@contextmanager
def page_session(
    config: ScraperConfig | None = None,
) -> Generator[Page, None, None]:
    """Single page, minimal API — typical for one-flow scrapers."""
    with browser_session(config) as _p, _b, page:
        yield page
