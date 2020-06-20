from GeniusArtistDataCollect import GeniusArtistDataCollect
from utils import stringifyLyrics 
import pandas as pd
import warnings
import os
import keyring
import markovify

ARTIST_NAME = 'John Mayer'
ALBUM = 'Continuum'

warnings.filterwarnings('ignore')

# Get the CSV file
if os.path.isfile('{}.csv'.format(ARTIST_NAME)):
	songs_df = pd.DataFrame.from_csv('{}.csv'.format(ARTIST_NAME))
else:
	# Get data
	client_access_token = keyring.get_password('api.genius.com', 'Genius Client Access Token')
	g = GeniusArtistDataCollect(client_access_token, ARTIST_NAME, ALBUM)
	songs_df = g.get_artist_songs()
	songs_df.to_csv('{}.csv'.format(ARTIST_NAME))

# Using Pandas dataframe, create string
lyrics = stringifyLyrics(songs_df)

# Markovify
text_model = markovify.NewlineText(lyrics)

for i in range(5):
    print(text_model.make_sentence())