import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl


@define
class LapGap:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "lapgap"

    def plot(self, **kwargs):
        data = self.dao.fetch_lapgaps(kwargs)
        print(data)
        return go.Figure().to_dict()
