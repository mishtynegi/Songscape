import requests
import pandas as pd
from bs4 import BeautifulSoup


def collect(link, start_year, end_year):
    data = pd.DataFrame(columns=['year', 'rank', 'artist'])
    year = end_year

    while year >= start_year:
        html_text = requests.get(link.format(year)).text
        soup = BeautifulSoup(html_text, "lxml")

        for item in soup.find_all("article", {"class": "ye-chart-item"}):
            rank = item.find(class_='ye-chart-item__rank').text.replace("\n", "").strip()
            artist = item.find(class_='ye-chart-item__title').text.replace("\n", "").strip()

            data = data.append({'year': year, 'rank': rank, 'artist': artist}, ignore_index=True)

        year -= 1

    return data


def main():
    artists = collect('https://www.billboard.com/charts/year-end/{:d}/top-artists', 2006, 2018)
    artists.to_csv('../data/artists_by_year.csv', index=False)


if __name__ == '__main__':
    main()
