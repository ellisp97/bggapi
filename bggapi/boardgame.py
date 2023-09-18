import xml.etree.ElementTree as ET
import requests
from utils import BoardgameUrls, PlayRecordParser


class Boardgame():
    """
    Class to extract the ID from the BGGAPI and perform subsequent queries using this ID
    https://boardgamegeek.com/wiki/page/BGG_XML_API2
    """
    def __init__(self, name: str):
        if not name:
            return None

        self.name = name
        self.boardgame_id = self.get_boardgame_id()
        self.df = None

        print(f"The ID for the boardgame {self.name} is {self.boardgame_id}.")

    def get_boardgame_id(self):
        response = requests.get(
            url=BoardgameUrls.SEARCH,
            params={
                "query": self.name,
                "exact": "1"
            })

        try:
            response_xml = ET.fromstring(response.content)
            # Process the XML data as needed
            # For example, you can extract specific information from the XML:
            if response_xml.findall(".//item"):
                # Process the XML data to extract the id
                for item in response_xml.findall(".//item"):
                    item_id = item.get("id")
                    if item_id:
                        return item.get("id")
                    else:
                        raise requests.RequestException("Board game not found.")
        except ET.ParseError as e:
            raise requests.RequestException("Error parsing XML response:", e)

    def get_play_history_df(self, query_params):
        self.df = PlayRecordParser(query_params)
