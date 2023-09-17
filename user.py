import requests

from utils import PlayRecordParser, BoardgameUrls


class User():
    """
    Class to query user play information, grouping by boardgames
    """
    def __init__(self, username: str):
        if not username:
            return None

        self.username = username
        self.boardgame_dict = self.group_boardgames()

    def group_boardgames(self) -> dict:
        df = PlayRecordParser({"username": self.username}).to_dataframe()

        # Filter only rows with 'boardgame' in the 'subtypes'
        boardgame_df = df[df['subtypes'].apply(lambda x: 'boardgame' in x)]
        unique_boardgames = boardgame_df['game_name'].unique()


        # Create a dictionary keyed by board game, with rows of play data as values
        boardgame_dict = {}
        for boardgame in unique_boardgames:
            boardgame_dict[boardgame.lower()] = df[df['game_name'] == boardgame]
        return boardgame_dict
