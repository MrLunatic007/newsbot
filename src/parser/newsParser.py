from typing import Optional

from bs4 import BeautifulSoup


class NewsParserError(Exception):
    """Gets raised when there is an error parsing the text"""

    pass


class NewsParser:
    def parse_article(self, raw_html: str) -> Optional[str]:
        """Parses the list of news got from the getter and returns the first article"""
        try:

            soup = BeautifulSoup(raw_html, "html.parser")
            paragraphs = soup.find_all("p")

            article = [p.get_text() for p in paragraphs]

            full_article = "\n".join(article)

            return full_article

        except Exception as e:
            raise NewsParserError(f"Could not parse text. Details {e}")
