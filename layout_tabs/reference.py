import dash_html_components as html
import dash_table
import pandas as pd
from app import app

df = pd.DataFrame()
df['KEY'] = ['duration_ms', 'key', 'mode', 'time_signature', 'acousticness', 'danceability',
             'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness',
             'valence', 'tempo', 'id', 'uri', 'track_href', 'analysis_url', 'type']

df['VALUE_TYPE'] = ['int', 'int', 'int', 'int', 'float', 'float', 'float',
                    'float', 'float', 'float', 'float', 'float', 'float',
                    'string', 'string', 'string', 'string', 'string']

df['VALUE_DESCRIPTION'] = ["The duration of the track in milliseconds.",
                           "The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.",
                           "Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.",
                           "An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).",
                           "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
                           "Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
                           "Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.",
                           "Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.",
                           "Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.",
                           "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db.",
                           "Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.",
                           "A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).",
                           "The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.",
                           "The Spotify ID for the track.",
                           "The Spotify URI for the track.",
                           "A link to the Web API endpoint providing full details of the track.",
                           "An HTTP URL to access the full audio analysis of this track. An access token is required to access this data.",
                           "The object type: \"audio_features\""]


def get_reference_data():
    return dash_table.DataTable(
        style_data={'whiteSpace': 'normal'},
        style_header={
            'fontWeight': 'bold'
        },
        style_cell={'textAlign': 'left'},
        css=[{
            'selector': '.dash-cell div.dash-cell-value',
            'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
        }],
        data=df.to_dict('rows'),
        columns=[{'id': c, 'name': c} for c in df.columns],
    )


content = html.Div([
    html.H4('Reference for audio analysis features'),
    html.Div(get_reference_data())
])
