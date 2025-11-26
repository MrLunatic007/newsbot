import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


class NewsGetterError(Exception):
    """Gets raised when an error occurs when getting News"""

    pass


class NewsGetter:
    def __init__(self, url: str) -> None:
        self.url = url

    def _robot_checker(self) -> bool:
        """Checks the robots.txt file to check if the page can be parsed"""
        try:
            parsed_url = urlparse(self.url)
            robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"

            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()

            user_agent: str = "newsagent"
            verification = rp.can_fetch(user_agent, self.url)

            return verification
        except Exception as e:
            print("Error when reading robot.txt file.")
            raise NewsGetterError(e)

    def fetch_html(self) -> str:
        """Gets the html from the url and returns paragraphs"""
        try:

            if not self._robot_checker():
                print("Robot file not parsed exiting")
                raise NewsGetterError("Scrapping forbidden by robots.txt")

            resp = requests.get(self.url, timeout=10)
            resp.raise_for_status()

            return resp.text

        except requests.RequestException as e:
            raise NewsGetterError(
                f"Error when getting news from {self.url}. Details: {e}"
            )
