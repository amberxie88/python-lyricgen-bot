import pandas as pd

def stringifyLyrics(songs_df: pd.DataFrame):
	lyrics = ""
	for ind in songs_df.index: 
		lyrics += songs_df['Lyrics'][ind]
	return lyrics 