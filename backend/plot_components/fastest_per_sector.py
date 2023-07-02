import fastf1
import numpy as np
import matplotlib as mpl
from attr import define

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from backend.dao.dao import TemporalContextAggregationImpl
from backend.plot_components.plot_utils.utils import get_two_driver_plot_color
import os

fastf1.Cache.enable_cache(os.getcwd())
import fastf1 as ff1
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
from scipy.stats import mode



@define
class FastestPerSector:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "fastest_per_sector"

    def plot(self, **kwargs):

        session = ff1.get_session(year=int(kwargs["year"]), gp=kwargs["gp"],identifier=kwargs["mode"])
        weekend = session.event
        session.load()

        driver_a = kwargs["driver_a"]
        driver_b = kwargs["driver_b"]

        lap = session.laps.pick_driver(driver_a).pick_fastest()
        circuit_ver = lap.telemetry[["X", "Y", "Speed"]]
        circuit_ver = circuit_ver.reset_index(drop=True)
        circuit_ver["Driver"] = driver_a

        lap = session.laps.pick_driver(driver_b).pick_fastest()
        circuit_alo = lap.telemetry[["X", "Y", "Speed"]]
        circuit_alo = circuit_alo.reset_index(drop=True)
        circuit_alo["Driver"] = driver_b

        circuit_final = pd.concat([circuit_ver, circuit_alo])
        df_sorted = circuit_final.sort_values('Speed')
        df_unique = df_sorted.drop_duplicates(['X', 'Y'], keep='first')
        df_unique = df_unique.sort_index("index")

        rolling = len(df_unique) // 5

        driver_1_color, driver_2_color = get_two_driver_plot_color(driver_a, driver_b, session)

        grouped = df_unique.groupby(df_unique.index // rolling)
        mode_values = grouped['Driver'].agg(lambda x: mode(x)[0][0])
        df_unique['MostFrequentDriver'] = mode_values.repeat(rolling).reset_index(drop=True)
        df_unique.loc[(df_unique['MostFrequentDriver'] == driver_a), 'Color'] = driver_1_color
        df_unique.loc[(df_unique['MostFrequentDriver'] == driver_b), 'Color'] = driver_2_color
        df_unique = df_unique.dropna()

        fig = go.Figure()

        init = 0
        for val in range(rolling, len(df_unique), rolling):
            tmp = df_unique[init:val]
            color = tmp["Color"].iloc[0]
            driver = tmp["MostFrequentDriver"].iloc[0]
            init = val
            fig.add_trace(go.Scatter(x=tmp["X"], y=tmp["Y"], mode="lines", marker_color=color,
                                     marker_size=0.5, line_width=2, line_shape="spline", name=driver, ))

        tmp = df_unique[init:len(df_unique)]
        fig.add_trace(go.Scatter(x=tmp["X"], y=tmp["Y"], mode="lines", marker_color=color,
                                 marker_size=0.5, line_width=2, line_shape="spline", name=driver, ))

        fig.update_layout(showlegend=True, plot_bgcolor="white", paper_bgcolor="white", margin=dict(l=0,r=0,t=0,b=0))
        range_x = [df_unique["X"].min() - 1000, df_unique["X"].max() + 1000]
        fig.update_xaxes(
            showticklabels=False,
            showgrid=False,
            range=range_x

        )
        fig.update_yaxes(
            showticklabels=False,
            showgrid=False, )
        fig.update_traces(connectgaps=True)

        names = set()
        fig.for_each_trace(
            lambda trace:
            trace.update(showlegend=False)
            if (trace.name in names) else names.add(trace.name))

        return fig.to_json()
