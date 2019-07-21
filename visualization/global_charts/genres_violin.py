import pandas as pd

highlights = ['dance pop', 'brill building pop', 'art rock', 'classic soul', 'classic rock',
              'contemporary country', 'disco', 'atl hip hop', 'bubblegum pop', 'boy band',
              'pop', 'alternative metal', 'hip hop']


data = pd.read_csv('./data/audio_feature.csv')
# genres = data.groupby(['genre']).size().sort_values(ascending=False)[:30]

violin_data = []
for genre in highlights:
    years = data[data['genre'] == genre]['year']
    trace = {
        "type": "violin",
        "x": [genre] * len(years),
        "y": years,
        "name": genre,
        "showlegend": False,
        "spanmode": "hard"
    }
    violin_data.append(trace)

fig = {
    "data": violin_data,
    "layout": {
        "title": "Genres Evolution",
        "yaxis": {
            "zeroline": False,
        }
    }
}
