"""
File: spotify.py
-------------------
Analyze and viasualize a Spotify user's listening history
"""

import spotipy
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import seaborn as sns

CLIENT_ID = '0bc764902f94469092ab888349da7d60'
CLIENT_SECRET = '44c8cf4a9d8745d1ab141a66eb52b728'
REDIRECT_URI = 'http://localhost:8888/callback/'
SCOPE = 'user-top-read'


def main():

    # authenticate user with Spotify
    username = input("\nPlease enter your Spotify username: ")
    token = spotipy.util.prompt_for_user_token(username,
                                               SCOPE,
                                               client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               show_dialog=True)
    sp = spotipy.Spotify(auth=token)
    print('Successfully authenticated! \n')

    # Spotify offers 3 time ranges over which you can pull a user's top songs
    ranges = ['short_term', 'medium_term', 'long_term']

    # Visualize data all in one window using subplots
    fig, axes = plt.subplots(3, 5, figsize=(18, 9.5), sharey='row')
    fig.suptitle(f'{username}\'s Spotify Data - Visualized by Time Period')
    plt.subplots_adjust(hspace=.5)

    for idx, range in enumerate(ranges):

        if range == 'short_term':
            time_period = 'In the past month'
        elif range == 'medium_term':
            time_period = 'In the past 6 months'
        else:
            time_period = 'Over all of your listening history'

        print(f"{time_period}, here were your top tracks...")
        results = sp.current_user_top_tracks(time_range=range, limit=50)

        # list of dicts, to be converted into dataframe
        top_songs = []
        for item in results['items']:

            # truncate song title and artist title if too long
            # (cited from https://stackoverflow.com/questions/2872512/python-truncate-a-long-string/34993870)
            if len(item['name']) > 35:
                item['name'] = (item['name'][:35] + '...')
            if len(item['artists'][0]['name']) > 25:
                item['artists'][0]['name'] = (
                    item['artists'][0]['name'][:25] + '...')

            # pull the metrics we want to analyze
            top_songs.append({
                'Title': item['name'],
                'Artist': item['artists'][0]['name'],
                'Popularity': item['popularity'],
                'Tempo': sp.audio_features(item['id'])[0]['tempo'],
                'Happiness': sp.audio_features(item['id'])[0]['valence'],
                'Energy': sp.audio_features(item['id'])[0]['energy'],
                'Acousticness': sp.audio_features(item['id'])[0]['acousticness']
            })

        top_songs_df = pd.DataFrame(top_songs)
        # start the df index from 1, not 0
        top_songs_df.index = top_songs_df.index + 1
        print(tabulate(top_songs_df, headers='keys', tablefmt='psql'))
        # skip a line
        print()

        # plot popularity
        sns.histplot(ax=axes[idx, 0],
                     data=top_songs_df['Popularity'], kde=True)

        # plot tempo
        sns.histplot(
            ax=axes[idx, 1], data=top_songs_df['Tempo'], color='green', kde=True)

        # plot happiness
        sns.histplot(ax=axes[idx, 2], data=top_songs_df['Happiness'],
                     color='orange', kde=True).set_title(time_period)

        # plot energy
        sns.histplot(
            ax=axes[idx, 3], data=top_songs_df['Energy'], color='yellow', kde=True)

        # plot acousticness
        sns.histplot(
            ax=axes[idx, 4], data=top_songs_df['Acousticness'], color='pink', kde=True)

    # show visualization
    plt.show()

    # accessibility
    print('Shown in the images: Histograms of your songs\' popularity, tempo, happiness, energy, and acousticness over each time period')


if __name__ == '__main__':
    main()
