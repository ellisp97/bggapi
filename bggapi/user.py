import pandas as pd
import numpy as np

from utils import PlayRecordParser, BoardgameUrls

class User():
    """
    Class to query user play information, grouping by boardgames
    """
    def __init__(self, username: str):
        self.username = username
        self.boardgame_dict = self.group_boardgames()

    def group_boardgames(self) -> dict:
        play_records = PlayRecordParser({"username": self.username})
        df = play_records.to_dataframe()

        # Filter only rows with 'boardgame' in the 'subtypes'
        boardgame_df = df[df['subtypes'].apply(lambda x: 'boardgame' in x)]
        unique_boardgames = boardgame_df['game_name'].unique()
        play_records.parse()
        # Create a dictionary keyed by board game, with rows of play data as values
        boardgame_dict = {}
        for boardgame in unique_boardgames:
            normalised_boardgame = self.normalise_boardgame_data( df[df['game_name'] == boardgame])
            boardgame_dict[boardgame] = normalised_boardgame.dropna(axis=1, how='all')

        return boardgame_dict

    def normalise_boardgame_data(self, boardgame_dict: pd.DataFrame):
        normalized_rows = []

        for play_id, row in boardgame_dict.iterrows():
            # Extract common columns (non-player-related)
            common_data = [play_id, row['date'], row['quantity'], row['incomplete'], row['game_name']]

            # Identify player-related columns dynamically
            player_columns = [col for col in row.keys() if col.endswith('_win')]

            # Iterate through player-related columns and create a row for each player
            for player_column in player_columns:
                player_name = player_column.split('_win')[0]  # Extract player name from the column name

                if np.isnan(row[player_column]): # Skip if nan, meaning player did not play
                    continue

                player_data = common_data.copy()

                try:
                    row[f'{player_name}_score'] = int(row[f'{player_name}_score'])
                except:
                    row[f'{player_name}_score'] = 0

                player_data.extend(
                    [row[player_column], row[f'{player_name}_score'], row[f'{player_name}_team'], player_name])
                normalized_rows.append(player_data)

        # Create a new DataFrame from the list of normalized rows
        pdf = pd.DataFrame(normalized_rows, columns=['play_id', 'date', 'quantity', 'incomplete', 'game_name', 'win', 'score','team', 'player'])
        return pdf
