import fastf1
import pandas as pd
import os
from attrs import define
from backend.dao.dao import TemporalContextAggregation


@define
class LapGapsIngestor:
    dao: TemporalContextAggregation

    def get_metadata(self):
        return "lapgap_ingestor"

    def ingest(self, **kwargs):
        year, country, mode = kwargs["year"], kwargs["country"], kwargs["mode"]
        fastf1.Cache.enable_cache(os.path.join(os.getcwd(), "cache"))
        sess = fastf1.get_session(year=year, gp=country, identifier=mode)
        sess.load()
        lap_data = pd.DataFrame(sess.laps)

        lap_counts = pd.DataFrame(lap_data.groupby("Driver")["LapNumber"].count())
        max_lap_count = lap_counts["LapNumber"].max()
        if mode == "Q":
            min_lap_count = max_lap_count // 10
        else:
            min_lap_count = max_lap_count // 2.5
        lap_counts = lap_counts[lap_counts["LapNumber"] >= min_lap_count]
        lap_df = lap_data[lap_data["Driver"].isin(lap_counts.index)]

        driver_df = pd.DataFrame(lap_df)
        driver_df["LapTime"] = driver_df["LapTime"].apply(lambda x: x.total_seconds())
        gap_df = driver_df.groupby("Driver")["LapTime"].mean().sort_values().reset_index()

        gap_df["SpeedMode"] = "Average"
        gap_df_fastest = driver_df.groupby("Driver")["LapTime"].min().sort_values().reset_index()
        gap_df_fastest["SpeedMode"] = "Fastest"
        final_df = pd.concat([gap_df, gap_df_fastest], axis=0).sort_values(by=["LapTime"])

        final_df = final_df.merge(sess.results[["FullName", "TeamName", "TeamColor", "DriverNumber", "Abbreviation"]],
                                  left_on="Driver", right_on="Abbreviation")
        final_df = final_df.drop(["Abbreviation"], axis=1)

        final_df["Event"] = mode
        final_df["GP"] = country
        final_df["Year"] = year
        final_df["TeamColor"] = "#" + final_df["TeamColor"]
        self.dao.write_data(final_df, "lapgaps")
        return "Ingestion Successful"
