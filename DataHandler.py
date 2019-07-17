import pandas as pd

import GLOBALS


class DataCleaner:

    _tweets_raw = None

    def __init__(self):
        with open(GLOBALS.FILE) as json_file:
            self._tweets_raw = pd.read_json(json_file)
        self._tweets_raw.drop_duplicates(subset=['id'], keep='first', inplace=True)


