import fastf1
import pandas as pd
import os
from attrs import define
from backend.dao.dao import TemporalContextAggregation
import uuid


@define
class ColorInfo:
    dao: TemporalContextAggregation

    def get_metadata(self):
        return "color_info"

    def ingest(self, **kwargs):
        year = kwargs["year"]
        fastf1.Cache.enable_cache(os.path.join(os.getcwd(), "cache"))
        sess = fastf1.get_session(year=year, gp=country, identifier=mode)
        sess.load()
        lap_data = pd.DataFrame(sess.laps)
        lap_counts = pd.DataFrame(lap_data.groupby("Driver")["LapNumber"].count())
        lap_counts = lap_counts[lap_counts["LapNumber"] >= 1]
        lap_df = lap_data[lap_data["Driver"].isin(lap_counts.index)]
        lap_df["Driver"].unique()
        final = sess.laps[["LapNumber", "Driver", "SpeedST"]].groupby("Driver").max().reset_index()
        final = final.merge(sess.results[["DriverNumber", "Abbreviation", "TeamName", "TeamColor"]], left_on="Driver",
                            right_on="Abbreviation")
        final = final.drop(["Abbreviation"], axis=1)
        final["Event"] = mode
        final["GP"] = country
        final["Year"] = year

        final["TeamColor"] = "#" + final["TeamColor"]

        final_types = final.dtypes

        def custom_uuid(data):
            val = uuid.uuid5(uuid.NAMESPACE_DNS, data)
            return val

        def create_uuid_on_n_col(df):
            temp = df.agg('_'.join, axis=1)
            return df.assign(id=temp.apply(custom_uuid))

        final = create_uuid_on_n_col(final.astype(str))
        final = final.astype(final_types)
        final["id"] = final["id"].astype(str)
        self.dao.write_data(final, "topspeed_st")
        return "Topspeed Ingestion Successful"
