# -*- coding: utf-8 -*-
"""Resources used to get Pokemon data and instantiate Pokemon"""

from typing import Any, Dict, List, Union
from urllib.parse import urljoin

import requests

from scyther.pokemon import Pokemon

# Create a JSON type (even though this isn't exact)
PokeJSON = Dict[str, Any]  # type: ignore # Allow this use of Any to avoid other ignores


# TODO: None of these have to be methods
class Pokedex:
    """Resource for fetching and caching pokemon data.

    Notes:
        Uses the v2 version of the API
        See https://pokeapi.co/docsv2/.
    """
    def __init__(self) -> None:
        # Base API URL. Could technically be overridden during init
        self._url = 'http://pokeapi.co/api/v2/'
        # Set what we consider the first and last pokemon
        self._min_num = 1
        self._max_num = 151

    def _cache(self, pokejson: PokeJSON) -> None:
        """Cache the pokemon response locally."""
        pass

    def _cache_get(self, num: int) -> Union[PokeJSON, None]:
        """Get a pokemon from the cache."""
        pass

    def fetch(self, num: int) -> PokeJSON:
        """Fetch data for the pokemon from the api."""
        url = urljoin(self._url, 'pokemon/{}'.format(num))
        return requests.get(url).json()  # type: ignore

    def get(self, num: int) -> PokeJSON:
        """Get a pokemon from the cache or the api.

        If not in the local cache, will externally request and cache the pokemon.
        """
        pokejson = self._cache_get(num)
        if pokejson is None:
            # TODO: Error handle and skip
            pokejson = self.fetch(num)
            self._cache(pokejson)
        return pokejson

    def get_all(self) -> List[PokeJSON]:
        """Get all pokemon within the min and max range."""
        return [self.get(i) for i in range(self._min_num, self._max_num)]
