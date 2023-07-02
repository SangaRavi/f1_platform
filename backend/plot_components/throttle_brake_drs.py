import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import fastf1
import os


@define
class ThrottleBrakeDRS:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "throttle_brake_drs"

    def plot(self, **kwargs):
        fastf1.Cache.enable_cache(os.getcwd())
        sess = fastf1.get_session(year=int(kwargs["year"]), gp=kwargs["gp"], identifier=kwargs["mode"])
        sess.load()

        laps_driver = sess.laps.pick_driver(kwargs["driver"])
        fastest_driver = laps_driver.pick_fastest()

        # Example timedelta
        td = fastest_driver.LapTime

        # Extracting lap time
        total_seconds = td.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        milliseconds = total_seconds % 1 * 1000

        lap_time = f"{minutes:02d}:{seconds:02d}.{milliseconds:.0f}"

        telemetry_driver_1 = fastest_driver.get_telemetry().add_distance()
        full_throttle = int(len(telemetry_driver_1[telemetry_driver_1["Throttle"]==100]) / len(telemetry_driver_1) * 100)
        full_brake = int(len(telemetry_driver_1[telemetry_driver_1["Brake"]==True]) / len(telemetry_driver_1) * 100)
        drs_open = int(len(telemetry_driver_1[telemetry_driver_1["DRS"]!=0]) / len(telemetry_driver_1) * 100)

        fig = go.Figure()

        fig.add_trace(go.Bar(y=["Full Throttle", "Full Brake", "DRS Active"], x=[100, 100, 100], orientation='h',
                             base=0, marker=dict(color="#DCDBDB"),
                             ))
        fig.add_trace(go.Bar(y=["Full Throttle", "Full Brake", "DRS Active"], x=[full_throttle, full_brake, drs_open], orientation='h',
                             #text=[f"{val}%" for val in [full_throttle, full_brake, drs_open]], textposition='inside',
                             marker=dict(color="#6C90FF")), )

        fig.update_layout(barmode="stack", bargap=0.8, paper_bgcolor='white', plot_bgcolor="white", showlegend=False,
                          xaxis=dict(showticklabels=False, showgrid=False),
                          yaxis=dict(autorange="reversed", showticklabels=False, showgrid=False))

        fig.add_annotation(x=0, y=-.2, text=f"<b>FULL THROTTLE - {full_throttle}%</b>",
                           align="center",
                           showarrow=False,
                           xref="paper",
                           font=dict(
                               family="Courier New, monospace",
                               size=16,
                               color="black"
                           ), )
        fig.add_annotation(x=0, y=.8, text=f"<b>FULL BRAKE - {full_brake}%</b>",
                           align="center",
                           showarrow=False,
                           xref="paper",
                           font=dict(
                               family="Courier New, monospace",
                               size=16,
                               color="black"
                           ), )
        fig.add_annotation(x=0, y=1.8, text=f"<b>DRS OPEN - {drs_open}%</b>",
                           align="center",
                           showarrow=False,
                           xref="paper",
                           font=dict(
                               family="Courier New, monospace",
                               size=16,
                               color="black"
                           ), )

        fig.add_annotation(x=-1, y=1.8, text="<b>LAPTIME %</b>",
                           align="center",
                           showarrow=False,
                           xref="paper",
                           font=dict(
                               family="Courier New, monospace",
                               size=16,
                               color="black"
                           ), )

        fig.update_yaxes(title="<b>LAPTIME %</b>", title_font=dict(
            family="Courier New, monospace",
            size=25,
            color="black"
        ))
        fig.update_layout(title=lap_time, title_font=dict(color="white"), margin=dict(r=35))
        dat = fig.to_json()
        import json
        data = json.loads(dat)
        print(data["layout"])
        return fig.to_json()
