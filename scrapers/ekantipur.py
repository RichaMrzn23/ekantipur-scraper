"""Ekantipur.com scraping routines."""

from __future__ import annotations

from scrapers.base import BaseScraper


class EkantipurScraper(BaseScraper):
    def scrape_entertainment(self, base_url: str = "https://ekantipur.com"):
        self.page.goto(base_url)
        self.dismiss_known_modals()

        self.page.wait_for_selector("text=मनोरञ्जन")
        self.page.click("text=मनोरञ्जन")
        self.page.wait_for_load_state("networkidle")
        self.dismiss_known_modals()

        articles = self.page.query_selector_all(".category-inner-wrapper")[:5]
        news_data = []

        for article in articles:
            try:
                title_el = article.query_selector("h2 a")
                title = title_el.text_content().strip() if title_el else None

                img_el = article.query_selector(".category-image img")
                if img_el:
                    image_url = img_el.get_attribute("src") or img_el.get_attribute(
                        "data-src"
                    )
                else:
                    image_url = None

                author_el = article.query_selector(".author-name a")
                author = author_el.text_content().strip() if author_el else None
            except Exception:
                title = None
                image_url = None
                author = None

            news_data.append(
                {
                    "title": title,
                    "image_url": image_url,
                    "category": "मनो रञ्जन",
                    "author": author,
                }
            )

        return news_data

    def scrape_cartoon(self, cartoon_url: str = "https://ekantipur.com/cartoon"):
        self.page.goto(cartoon_url)
        self.page.wait_for_load_state("networkidle")

        try:
            img_el = self.page.query_selector(".cartoon-image img")
            title = img_el.get_attribute("alt") if img_el else None
            image_url = img_el.get_attribute("src") if img_el else None
            cartoon_data = {
                "title": title,
                "image_url": image_url,
                "author": None,
            }
        except Exception:
            cartoon_data = {
                "title": None,
                "image_url": None,
                "author": None,
            }

        return cartoon_data
