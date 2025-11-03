import sys
import csv
import requests
from bs4 import BeautifulSoup
from typing import List


def fetch_html(url: str) -> BeautifulSoup:

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_main_table(soup: BeautifulSoup) -> List[List[str]]:

    rows = soup.find_all("tr")
    result = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 3:
            code = cells[0].get_text(strip=True)
            name = cells[1].get_text(strip=True)
            link = cells[0].find("a")
            href = f"https://www.volby.cz/pls/ps2017nss/{link['href']}" if link else ""
            result.append([code, name, href])
    return result


def parse_detail_page(url: str) -> List[str]:


    soup = fetch_html(url)


    stats_table = soup.find("table", class_="table")  # nebo podle konkrétní tabulky
    stats = []
    for row in stats_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 2:
            label = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True).replace("\xa0", "")
            if label in ["Voliči v seznamu", "Vydané obálky", "Platné hlasy"]:
                stats.append(value)


    votes_table = soup.find_all("table")[2]  # zpravidla 3. tabulka obsahuje hlasy
    party_votes = []
    for row in votes_table.find_all("tr")[1:]:  # přeskočíme hlavičku
        cells = row.find_all("td")
        if len(cells) >= 2:
            count = cells[1].get_text(strip=True).replace("\xa0", "")
            party_votes.append(count)

    return stats + party_votes


def save_to_csv(data: List[List[str]], header: List[str], output_file: str) -> None:

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)


def main() -> None:
    if len(sys.argv) != 3:
        print("❌ Použití: python scraper.py <url> <výstupní_soubor.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    try:
        main_soup = fetch_html(url)
        obce = parse_main_table(main_soup)

        all_data = []

        # hlavička CSV
        header = ["Kód obce", "Název obce", "Voliči v seznamu", "Vydané obálky", "Platné hlasy"]

        # zjistíme počet stran podle první obce
        if obce:
            first_detail = parse_detail_page(obce[0][2])
            num_parties = len(first_detail) - 3
            for i in range(1, num_parties + 1):
                header.append(f"Strana {i}")

        # pro všechny obce
        for code, name, link in obce:
            if link:
                detail = parse_detail_page(link)
                all_data.append([code, name] + detail)

        save_to_csv(all_data, header, output_file)
        print(f"✅ Výsledky uloženy do: {output_file}")

    except requests.exceptions.RequestException:
        print("❌ Chyba: zadaný odkaz není platný nebo web není dostupný.")
        sys.exit(1)


if __name__ == "__main__":
    main()
