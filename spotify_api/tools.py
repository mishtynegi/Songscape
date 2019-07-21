import requests
import pandas as pd
import time
import math
from data_collection import postprocessing

authorization_token = 'Bearer BQAV9Xqs1X_JdKPSBSZ6tA07NYugJaiPcA6QD3KsVuWacFVeUfuQnhJHXEBrQ_5sdZKuVFHiBInwQkkq6of3AvHQgUy80WZXLMZgzTiR0hE3bGyxHKo69qwZ37c_5jK5EeMksPw7Yx4'


def get_track(auth_token, id, market):
    params = {'market': market}
    song_id = id
    headers = {'Authorization': auth_token}
    return requests.get(url = 'https://api.spotify.com/v1/tracks/'+song_id, params=params, headers=headers)


def get_several_tracks(auth_token, ids):
    params = {'ids': ids}
    headers = {'Authorization': auth_token}
    return requests.get(url='https://api.spotify.com/v1/tracks', params=params, headers=headers)


def search_track(auth_token, q, type, limit=10, offset=5):
    params = {'q': q, 'type': type, 'limit': limit, 'offset': offset}
    headers = {'Authorization': auth_token}
    return requests.get(url = 'https://api.spotify.com/v1/search', params=params, headers=headers)


def get_artist(auth_token, id):
    headers = {'Authorization': auth_token}
    artist_id = id
    return requests.get(url = 'https://api.spotify.com/v1/artists/'+artist_id, headers=headers)


def get_audio_feature_for_tracks(auth_token, ids):
    params = {'ids': ids }
    headers = {'Authorization': auth_token }
    return requests.get(url='https://api.spotify.com/v1/audio-features', params=params, headers=headers)


def get_audio_feature_for_a_track(auth_token, id):
    headers = {'Authorization': auth_token}
    song_id = id
    return requests.get(url='https://api.spotify.com/v1/audio-features/'+song_id, headers=headers)


def audio_analysis_for_a_track(auth_token, id):
    headers = {'Authorization': auth_token }
    song_id = id
    return requests.get(url='https://api.spotify.com/v1/audio-analysis/'+song_id, headers=headers)


def retrieve_tracks_id(path):
    '''
    if using global weekly lastest, use the following code to retrieve url

    file = pd.read_csv(path)
    track_url = file.iloc[:, 4].str[31:]

    tmp = []
    for url in track_url:
       tmp.append(str(url))

    return tmp[1:]
    '''

    file = pd.read_csv(path)

    track, artist = file["title"], file["artist1"]
    track_id = []
    dead_track = []
    for i in range(0, len(track)):
        q = '"' + track[i] + '"' + ',' + '"' + artist[i] + '"'

        # print current progress
        if i % 100 == 0:
            print (i)

        try:
            tmp = search_track(authorization_token, q, 'track', 1, 0).json()
            track_id.append(tmp['tracks']['items'][0]['id'])

        except IndexError as e:
            # handling exception of not find the track on spotify
            dead_track.append(i+2)
            track_id.append("Not in Spotify")

        except:
            # handling exception for sending to much request
            if tmp['error']['status'] == 429:
                time.sleep(3)
                tmp = search_track(authorization_token, q, 'track', 1, 1).json()
                track_id.append(tmp['tracks']['items'][0]['id'])
            else:
                print(tmp['error']['status'])

    print ("ok")

    print("song id: " )
    for item in dead_track:
        print (item)
    print("are dead")

    return track_id


def fun_test():
    assert get_track(authorization_token, '11dFghVXANMlKmJXsNCbNl', 'ES').text
    assert search_track(authorization_token, 'Muse', 'track,artist', 10, 5).text
    assert get_artist(authorization_token, '0TnOYISbd1XYRBk9myaseg').text
    assert get_audio_feature_for_tracks(authorization_token,
                                        '7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ,2takcwOaAZWiXQijPHIx7B, ,').text
    assert audio_analysis_for_a_track(authorization_token, '11dFghVXANMlKmJXsNCbNl').text


if __name__ == '__main__':

    '''
    # get all track id from path
    path = "../data/top_by_year.csv"
    tracks_url = retrieve_tracks_id(path)

    
    # store track id
    tracks_df = pd.DataFrame(tracks_url, columns=["id"])
    tracks_df.to_csv('track_url_1.csv', index=False)

    '''
    # initialize variables for audio analysis
    tracks_url = pd.read_csv("track_url_1.csv")['id'].values.tolist()
    ids = ''
    count = 0

    '''
    # audio analysis on songs
    df = pd.DataFrame()
    song_info = pd.DataFrame
    for url in tracks_url:
        if url == "Not in Spotify":
            ids += " ,"
            count += 1
            continue

        ids += str(url) + ','
        count += 1
        if count == 100:
            result = get_audio_feature_for_tracks(authorization_token, ids).json()
            try:
                for feature in result['audio_features']:
                    if feature == None:
                        df = df.append({"status": "404: analysis not found"}, ignore_index=True)
                    else:
                        df = df.append(feature, ignore_index=True)
                count = 0
                ids = ''
            except:
                print (result['error']['status'], result['error']['message'])
    # calculate result for the final set of songs
    result = get_audio_feature_for_tracks(authorization_token, ids).json()
    try:
        for feature in result['audio_features']:
            if feature == None:
                df = df.append({"status": "404: analysis not found"}, ignore_index=True)
            else:
                df = df.append(feature, ignore_index=True)
        count = 0
        ids = ''
    except:
        print(result['error']['status'], result['error']['message'])

    # append song name and artist name to the data
    top_by_year = pd.read_csv("../data/top_by_year.csv")
    df['artist1'] = top_by_year['artist1']
    df['artist2'] = top_by_year['artist2']
    df['artist3'] = top_by_year['artist3']
    df['artist4'] = top_by_year['artist4']
    df['artist5'] = top_by_year['artist5']
    df['artist6'] = top_by_year['artist6']
    df['title'] = top_by_year['title']

    df.to_csv("../data/top_by_year-AUDIO_FEATURE_1.csv", index=False)

    '''

    # save track information
    ids = ''
    count = 0
    df1 = pd.DataFrame()
    for url in tracks_url:
        if url == "Not in Spotify" and len(ids) > 0:
            tracks_info = get_several_tracks(authorization_token, ids[:-1]).json()
            # append previous stored tracks
            try:
                for track in tracks_info['tracks']:
                    df1 = df1.append(track, ignore_index=True)
                # reset counter and append the empty track
                count = 0
                ids = ''
                df1 = df1.append({"no_track": "No track is found."}, ignore_index=True)
                continue
            except:
                print(tracks_info['error']['status'], tracks_info['error']['message'])

        ids += str(url) + ','
        count += 1
        if count == 30:
            try:
                tracks_info = get_several_tracks(authorization_token, ids[:-1]).json()
                for track in tracks_info['tracks']:
                    df1 = df1.append(track, ignore_index=True)
                count = 0
                ids = ''
            except:
                print(tracks_info['error']['status'], tracks_info['error']['message'])

    # get track info for remainder
    if len(ids) > 0:
        tracks_info = get_several_tracks(authorization_token, ids[:-1]).json()
        for track in tracks_info['tracks']:
            df1 = df1.append(track, ignore_index=True)
        count = 0
        ids = ''

    df1.to_csv("../data/top_by_year-TRACK_INFO.csv", index=False)

