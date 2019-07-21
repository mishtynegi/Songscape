import time
import requests
import pandas as pd

from data_collection.key import key

authorization_token = 'Bearer ' + key


def search_item(name, type_, limit=1, offset=0):
    header = {'Authorization': authorization_token}
    params = {'q': name, 'type': type_, 'limit': limit, 'offset': offset}
    res = requests.get(url='https://api.spotify.com/v1/search', params=params, headers=header)

    if res.status_code == 429:
        raise RuntimeError()
    elif res.status_code != 200:
        raise ValueError(str(res.status_code) + " " + res.json()['error']['message'])

    res = res.json()['artists']['items']
    if not len(res):
        raise ValueError('Unknown artist: ' + name)

    return res[0]


def main():
    artists = pd.read_csv('../data/artists_by_year.csv')

    for i, row in artists.iterrows():
        try:
            data = search_item(row['artist'], type_='artist')
        except RuntimeError:
            time.sleep(5)
            data = search_item(row['artist'], type_='artist')

        artists.at[i, 'id'] = data['id']
        artists.at[i, 'genres'] = data['genres']
        artists.at[i, 'popularity'] = data['popularity']
        artists.at[i, 'followers'] = data['followers']['total']

    artists['popularity'] = artists['popularity'].astype(int)
    artists['followers'] = artists['followers'].astype(int)

    artists.to_csv('../data/artists_by_year.csv', index=False)


if __name__ == '__main__':
    main()
