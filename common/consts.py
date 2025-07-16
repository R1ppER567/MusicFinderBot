from typing import Final

NUM_OF_RESULTS: Final = 20
TRACKS_PER_PAGE: Final = 8
FIRST_PAGE: Final = 1
LAST_PAGE: Final = -(-NUM_OF_RESULTS // TRACKS_PER_PAGE)
