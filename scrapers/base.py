"""Shared helpers for Playwright-based scrapers."""

from playwright.sync_api import Page


class BaseScraper:
    def __init__(self, page: Page) -> None:
        self.page = page

    def dismiss_known_modals(self) -> None:
        """Remove common overlay / paywall UI if present."""
        self.page.wait_for_timeout(2000)
        self.page.evaluate(
            """
            const modal = document.querySelector('#pagegate');
            if (modal) modal.remove();

            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) backdrop.remove();

            document.body.classList.remove('modal-open');
            """
        )
