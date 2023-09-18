import pandas as pd
import xml.etree.ElementTree as ET
import requests


class BoardgameUrls():
    BASE_URL = "https://boardgamegeek.com/xmlapi2"

    SEARCH = f"{BASE_URL}/search"
    PLAY_HISTORY = f"{BASE_URL}/plays"
    THING = f"{BASE_URL}/thing"
    COLLECTION = f"{BASE_URL}/collection"
    GUILD = f"{BASE_URL}/guild"

class PlayRecordParser:
    def __init__(self, query_params):
        self.query_params = query_params
        self.all_records = []
        self.max_pages = 10
        self.parse()

    def fetch_data(self, page):
        self.query_params['page'] = page
        response = requests.get(url=BoardgameUrls.PLAY_HISTORY, params=self.query_params)

        if response.status_code == 200:
            parser = ET.XMLParser(encoding="utf-8")
            root = ET.fromstring(response.content, parser=parser)

            for play in root.findall('play'):
                play_data = {
                    'play_id': play.get('id'),
                    'user_id': play.get('userid'),
                    'date': play.get('date'),
                    'quantity': play.get('quantity'),
                    'incomplete': play.get('incomplete'),
                }

                item = play.find('item')
                if item is not None:
                    play_data['game_name'] = item.get('name')
                    play_data['object_type'] = item.get('objecttype')
                    play_data['object_id'] = item.get('objectid')

                    subtypes_element = item.find('subtypes')
                    if subtypes_element is not None:
                        subtypes_list = [subtype.get('value') for subtype in subtypes_element.findall('subtype')]
                        play_data['subtypes'] = subtypes_list

                # Store data from the comments tag
                comments_element = play.find('comments')
                if comments_element is not None:
                    play_data['comments'] = comments_element.text.strip()

                # Store data from the players tag
                players_element = play.find('players')
                if players_element is not None:
                    players_data = []
                    for player in players_element.findall('player'):
                        player_data = {
                            'username': player.get('username'),
                            'userid': player.get('userid'),
                            'name': player.get('name'),
                            'color': player.get('color'),
                            'score': player.get('score'),
                            'win': player.get('win')
                        }
                        players_data.append(player_data)

                    player_names = [player['name'] for player in players_data]
                    player_scores = [player['score'] for player in players_data]
                    player_wins = [player['win'] == '1' for player in players_data]

                    # Creating a dictionary to store the results
                    player_dict = {name + '_score': score for name, score in zip(player_names, player_scores)}
                    player_dict.update({name + '_win': win for name, win in zip(player_names, player_wins)})

                    # Add the player_dict to data
                    play_data.update(player_dict)

                self.all_records.append(play_data)
        else:
            print(f"Failed to fetch data from page {page}. Status code: {response.status_code}")

    def parse(self):
        page = 1
        while page < self.max_pages:
            self.fetch_data(page)
            num_records = len(self.all_records)

            if num_records > 0 and num_records % 100 == 0:
                # Continue fetching if the number of records is a multiple of 100 (indicating there might be more pages)
                page += 1
            else:
                # If the number of records fetched in the current page is less than 100 or 0,
                # it means we have reached the last page, so break the loop.
                break

    def to_dataframe(self):
        return pd.DataFrame(self.all_records)