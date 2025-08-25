# bio_wordle_wordlist.py

import requests
from bs4 import BeautifulSoup

# URLs to scrape
URLS = [
    "https://staphb.org/resources/2019-12-18-binfo_glossary.html",
    "https://www.biosyn.com/bioinformatics.aspx"
]

# Expanded curated 5-letter biology/bioinformatics terms
CURATED_TERMS = {
    "blast", "reads", "motif", "align", "probe", "graph", "locus", "omics",
    "spike", "genes", "cells", "helix", "crisp", "plasm", "exons", "intro",
    "folds", "phase", "rad51", "rnaas", "dnaas", "orbit", "biome", "cysts",
    "flora", "fauna", "amino", "plant", "virus", "fungi", "bonds", "rnaes",
    "spore", "heart", "blood", "brain", "stem", "gland", "organ", "leafy","agent","drugs","exons"
}


def extract_terms(url):
    """Scrape terms and keep only *real* 5-letter alphabetic words."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    terms = []
    for tag in soup.find_all(['strong', 'b']):
        raw = tag.get_text(strip=True)
        if not raw:
            continue
        # Take only the whole word (not split/truncate)
        if raw.isalpha() and len(raw) == 5:
            terms.append(raw.lower())
    return terms


def build_word_list():
    # Scrape all terms
    scraped_terms = set()
    for url in URLS:
        scraped_terms.update(extract_terms(url))

    print(f"Scraped {len(scraped_terms)} valid 5-letter words.")

    # Merge with curated list
    final_terms = sorted(scraped_terms.union(CURATED_TERMS))
    print(f"Final word list has {len(final_terms)} words.")

    # Save to file
    with open("bio_wordle_list.txt", "w", encoding="utf-8") as f:
        for term in final_terms:
            f.write(term + "\n")


if __name__ == "__main__":
    build_word_list()

