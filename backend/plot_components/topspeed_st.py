import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import plotly.express as px


@define
class TopSpeedST:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "topspeed_st"

    def plot(self, **kwargs):
        data = self.dao.fetch_data_from_table(kwargs, "topspeed_st")
        data = data.sort_values(by="speedst", ascending=False)
        min_range = data["speedst"].min() * 0.98
        max_range = data["speedst"].max() * 1.02
        # st.markdown(f'### {laptime_selection}')
        fig = px.bar(data, x="driver", y="speedst", color="driver", text_auto='.s',
                     color_discrete_map=dict(zip(data["driver"], data["teamcolor"])))
        fig.update_yaxes(range=[min_range, max_range], title="Topspeed at Speed Trap", showline=True, linecolor='black',
                         gridcolor='lightgrey')
        fig.update_xaxes(title="", showline=True, linecolor='black', gridcolor='lightgrey')
        fig.update_layout(showlegend=False, title="", title_x=0.5, plot_bgcolor='white')
        return fig.to_json()
