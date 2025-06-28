import requests
from bs4 import BeautifulSoup
import re


BASE_URL = "https://hmdb.ca"
SEARCH_URL = f"{BASE_URL}/unearth/q"


def search_metabolite_url(query):
    print(f"Searching HMDB for: {query}")
    res = requests.get(SEARCH_URL, params={"query": query, "searcher": "metabolites"})
    soup = BeautifulSoup(res.text, "html.parser")

    result = soup.select_one("a[href^='/metabolites/']")
    if not result:
        raise ValueError("No metabolite match found.")
    return BASE_URL + result["href"]


def get_first_spectrum_url(metabolite_url):
    print(f"Fetching metabolite page: {metabolite_url}")
    res = requests.get(metabolite_url)
    soup = BeautifulSoup(res.text, "html.parser")

    spectrum_link = soup.find("a", string="View Spectrum")
    if not spectrum_link:
        raise ValueError("No 'View Spectrum' link found.")
    return BASE_URL + spectrum_link["href"]


def get_first_txt_download_url(spectrum_url):
    print(f"Fetching spectrum page: {spectrum_url}")
    res = requests.get(spectrum_url)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find the table row by cell text, then the link
    row = soup.find("td", string=re.compile(r"List of m/z values"))
    if not row:
        raise ValueError("Spectrum description cell not found")

    parent_row = row.find_parent("tr")
    link = parent_row.find("a", href=re.compile(r"\.txt(\?|$)"))
    if not link:
        raise ValueError("No .txt download link found in spectrum row")

    href = link["href"]
    return href if href.startswith("http") else link.prettify()  # adjust if needed


def fetch_spectrum_data_from_txt(txt_url):
    print(f"Fetching TXT file: {txt_url}")
    res = requests.get(txt_url)
    lines = res.text.strip().splitlines()

    spectrum = []
    for line in lines:
        try:
            mz, intensity = map(float, line.split())
            spectrum.append((mz, intensity))
        except ValueError:
            continue  # skip malformed lines or headers
    return spectrum


def fetch_hmdb_spectrum(metabolite_name):
    try:
        metabolite_url = search_metabolite_url(metabolite_name)
        spectrum_url = get_first_spectrum_url(metabolite_url)
        txt_url = get_first_txt_download_url(spectrum_url)
        data = fetch_spectrum_data_from_txt(txt_url)
        print(f"Retrieved {len(data)} spectrum data points.")
        return data
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    name = input("Enter metabolite name: ").strip()
    data = fetch_hmdb_spectrum(name)
    for mz, intensity in data:
        print(f"m/z: {mz:.4f} | intensity: {intensity:.4f}")
