import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
from urllib.parse import urljoin  # Import for handling relative URLs


class URLGeneratorError(Exception):
    """Gets raised when generating urls"""

    pass


class URLGenerator:
    SITES: Dict[str, Dict[str, str]] = {
        "bbc": {
            "url_format": "https://www.bbc.co.uk/search?q={topic}&scope=news",
            "selector": "a.ssrcss-1u17s3s-PromoLink",
            "base_url": "https://www.bbc.co.uk",
        },
        # TODO: Add more sites (with their respective base_url and selector)
    }

    def generate_article_url(self, topic: str, site: str) -> str:
        """Generates an article url based on the site and topic"""
        try:
            source: Optional[Dict[str, str]] = self.SITES.get(site.lower())

            if not source:
                raise URLGeneratorError(
                    f"Site Error: {site} not supported by search source."
                )

            search_topic = requests.utils.quote(topic)
            search_url = source["url_format"].format(topic=search_topic)

            response = requests.get(search_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            url_link = soup.select_one(source["selector"])

            if url_link and url_link.get("href"):
                raw_url = url_link.get("href")

                base_url = source.get("base_url", "")
                full_url = urljoin(base_url, raw_url)

                return full_url
            else:
                raise URLGeneratorError(
                    f"No valid article found on the search page for {site}"
                )

        except requests.exceptions.Timeout as e:
            raise URLGeneratorError(
                f"Timed out: Check your connection and try again. Details: {e}"
            )
        except requests.exceptions.RequestException as e:
            raise URLGeneratorError(
                f"Network or HTTP error during search for {site}. Details: {e}"
            )
        except Exception as e:
            raise URLGeneratorError(f"Unknown error: {e}")
