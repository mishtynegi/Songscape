import os
import re
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup


def by_month(link, start_date):
    # set the initial date to the closest Saturday
    date = datetime.date.today() + datetime.timedelta(days=(5 - datetime.datetime.today().weekday()))

    while date >= start_date:
        html_text = requests.get(link + date.strftime('%Y-%m-%d')).text
        soup = BeautifulSoup(html_text, "lxml")

        for song in soup.find_all("div", {"class": "chart-list-item"}):
            print(song['data-rank'] + '\t' + song['data-artist'] + '\t' + song['data-title'])

        date = date - datetime.timedelta(days=7)


def by_year_process(data):
    data = data.rename(columns={'artist': 'artist1'})

    for index, row in data.iterrows():
        artists = re.split(
            ' X | x | / | & | Feat. | feat. | feat | featuring | Featuring | and | , | Duet | With | Or | And',
            row['artist1'])
        for i in range(len(artists)):
            data.at[index, 'artist' + str(i + 1)] = artists[i]

    return data


def by_year_old(path_old):
    data = pd.DataFrame(columns=['year', 'rank', 'artist', 'title'])

    for file in os.listdir(path_old)[::-1]:
        df = pd.read_csv(path_old + file)
        df = df.rename(columns={df.columns[0]: "rank", df.columns[1]: "artist", df.columns[2]: "title"})
        df = pd.concat([pd.DataFrame({'year': [int(file[0:4])] * len(df.index)}), df], axis=1)
        data = data.append(df, ignore_index=True)

    return data


def by_year(link, start_year, end_year):
    data = pd.DataFrame(columns=['year', 'rank', 'artist', 'title'])
    year = end_year

    while year >= start_year:
        html_text = requests.get(link.format(year)).text
        soup = BeautifulSoup(html_text, "lxml")

        for song in soup.find_all("article", {"class": "ye-chart-item"}):
            rank = song.find(class_='ye-chart-item__rank').text.replace("\n", "").strip()
            artist = song.find(class_='ye-chart-item__artist').text.replace("\n", "").strip()
            title = song.find(class_='ye-chart-item__title').text.replace("\n", "").strip()

            data = data.append({'year': year, 'rank': rank, 'artist': artist, 'title': title}, ignore_index=True)

        year -= 1

    return data


def main():
    # by_month('https://www.billboard.com/charts/hot-100/', datetime.date(2000, 1, 1))
    data_by_year = by_year('https://www.billboard.com/charts/year-end/{:d}/hot-100-songs', 2006, 2018)
    data_by_year = data_by_year.append(by_year_old("../data/billboard_old/"), ignore_index=True)
    data_by_year = by_year_process(data_by_year)

    data_by_year.to_csv('../data/top_by_year.csv', index=False)


if __name__ == '__main__':
    main()
