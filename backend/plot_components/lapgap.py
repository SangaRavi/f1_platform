import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import plotly.express as px


@define
class LapGap:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "lapgap"

    def plot(self, **kwargs):
        data = self.dao.fetch_data_from_table(kwargs, "lapgaps")
        if kwargs["mode"] == "fast":
            data = data[data["speedmode"] == "Fastest"]
        else:
            data = data[data["speedmode"] == "Average"]

        data = data.sort_values(by="laptime")
        min_range = data["laptime"].min() * 0.98
        max_range = data["laptime"].max() * 1.02
        fig = px.bar(data, x="driver", y="laptime", color="driver",
                     color_discrete_map=dict(zip(data["driver"], data["teamcolor"])))
        fig.update_yaxes(range=[min_range, max_range], title="LapTime in Seconds", showline=True, linecolor='black',
                         gridcolor='lightgrey')
        fig.update_xaxes(title="", showline=True, linecolor='black', gridcolor='lightgrey')
        fig.update_layout(showlegend=False, title="", title_x=0.5, plot_bgcolor='white')
        return fig.to_json()
