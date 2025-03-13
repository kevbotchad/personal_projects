import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def download_images(url, folder="cards"):
    # Create a folder to save images if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    print(f"Found {len(img_tags)} images. Starting download...")

    for i, img in enumerate(img_tags, start=1):
        img_url = img.get("src")
        if not img_url:
            continue

        # Convert relative URLs to absolute URLs
        img_url = urljoin(url, img_url)

        # Try to extract a valid filename from the URL
        filename = os.path.basename(img_url)
        if not filename:
            filename = f"image_{i}.jpg"  # Fallback to a generic name

        filepath = os.path.join(folder, filename)

        try:
            print(f"Downloading image {i}: {img_url}")
            img_response = requests.get(img_url)
            img_response.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(img_response.content)
        except requests.RequestException as e:
            print(f"Failed to download {img_url}: {e}")

if __name__ == "__main__":
    website_urls = ["https://metazoohq.com/cards/cryptid-nation/2nd-edition", "https://metazoohq.com/cards/cryptid-nation/decks", "https://metazoohq.com/cards/cryptid-nation/boxtoppers", "https://metazoohq.com/cards/cryptid-nation/nightfall/1st-edition", "https://metazoohq.com/cards/cryptid-nation/nightfall/decks", "https://metazoohq.com/cards/cryptid-nation/wilderness/1st-edition", "https://metazoohq.com/cards/cryptid-nation/wilderness/decks", "https://metazoohq.com/cards/cryptid-nation/ufo/1st-edition", "https://metazoohq.com/cards/cryptid-nation/seance/1st-edition", "https://metazoohq.com/cards/cryptid-nation/native/1st-edition"]
    for website_url in website_urls:
        download_images(website_url)
