import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import pandas as pd


@define
class Speeds:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "speeds"

    def plot(self, **kwargs):
        data = pd.read_csv("G:\Projects\\f1_platform\\backend\plot_components\spain_speed.csv")
        data = data.sort_values(by="Average Speed", ascending=False)
        min_range = data["Average Speed"].min() * 0.98
        max_range = data["Average Speed"].max() * 1.02
        fig = px.bar(data, x="Driver", y="Average Speed", color="Driver")
        fig.update_yaxes(range=[min_range, max_range], title="Average Speed in KPH", showline=True, linecolor='black',
                         gridcolor='lightgrey')
        fig.update_xaxes(title="", showline=True, linecolor='black', gridcolor='lightgrey')
        fig.update_layout(showlegend=False, title="", title_x=0.5, plot_bgcolor='white')
        return fig.to_json()
