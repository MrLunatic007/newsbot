import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")


def get_article_url():
    response = requests.get("https://bbc.com/news")
    soup = BeautifulSoup(response.content, "html.parser")

    # Get first few headline links
    candidates = soup.select("a:has(h2)")[:5]
    print(f"Found {len(candidates)} headline candidates")

    for link in candidates:
        href = link.get("href")
        if href and href.startswith("/news/articles/"):
            print(f"Selected article link: {href}")
            return href

    print("No valid article link found")
    return None


def get_article_text(url):
    if url.startswith("http"):
        full_url = url
    else:
        full_url = urljoin("https://bbc.com", url)
    # fetch full article page
    res = requests.get(full_url)
    print(f"Fetching: {full_url}")
    print(f"Status code: {res.status_code}")

    # extract <p> text
    soup = BeautifulSoup(res.content, "html.parser")
    context = soup.find("article")
    print(f"Found article section: {context is not None}")

    if context:
        par = context.find_all("p")
        print(f"Found {len(par)} paragraphs")
        if par:
            text = "\n".join([p.text for p in par])
            if not text.strip():
                print("Article text is empty")
                return None
            print(f"Text Length: {len(text) if text else 'None'}")
            return text
        else:
            return None
    else:
        return None


def summarize(text):
    client = InferenceClient(provider="hf-inference", api_key=HF_TOKEN)

    result = client.summarization(text, model="cnicu/t5-small-booksum")
    return result


def main():
    url = get_article_url()
    text = get_article_text(url)
    if not text:
        print("No article to summarize")
        return
    summary = summarize(text)
    print("URL:", url)
    print("SUMMARY:", summary)


if __name__ == "__main__":
    main()
