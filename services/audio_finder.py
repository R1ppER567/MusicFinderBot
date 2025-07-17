from ytmusicapi import YTMusic

from common.consts import NUM_OF_RESULTS

yt = YTMusic()


def search_music(query: str) -> list[dict]:
    """Searches for music tracks based on the provided query.

    Args:
        query (str): The search query string.
        num_of_results (int, optional): The number of results to return. 
        Defaults to 20.

    Returns:
        list[dict]: A list of dictionaries containing information about 
        the found tracks.
    """
    results = yt.search(query, filter='songs')
    return results[:NUM_OF_RESULTS]
