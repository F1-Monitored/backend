import fastf1

from app.core.config import FASTF1_CACHE

fastf1.Cache.enable_cache(FASTF1_CACHE)


class FastF1Client:

    @staticmethod
    def load_session(year: int, grand_prix: str, session: str):
        """
        Example:
        load_session(2024, "Monaco", "R")
        """
        race = fastf1.get_session(year, grand_prix, session)
        race.load()
        return race