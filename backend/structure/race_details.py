import pandas as pd
from attrs import define

@define
class RaceDetails:
    def countries(self, year) -> list:
        return ["Spain", "Bahrain"]
