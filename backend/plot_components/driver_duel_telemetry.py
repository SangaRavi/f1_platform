import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import fastf1
from fastf1 import utils
import os
from backend.plot_components.plot_utils.utils import get_two_driver_plot_color


@define
class DriverDuelTelemetry:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "driver_duel_telemetry"

    def plot(self, **kwargs):
        fastf1.Cache.enable_cache(os.getcwd())
        sess = fastf1.get_session(year=int(kwargs["year"]), gp=kwargs["gp"], identifier=kwargs["mode"])
        sess.load()

        driver_1, driver_2 = kwargs["driver_1"], kwargs["driver_2"]

        laps_driver_1 = sess.laps.pick_driver(driver_1)
        laps_driver_2 = sess.laps.pick_driver(driver_2)

        # Select the fastest lap
        fastest_driver_1 = laps_driver_1.pick_fastest()
        fastest_driver_2 = laps_driver_2.pick_fastest()

        # fastest_driver_1 = laps_driver_1[laps_driver_1['LapNumber'] == 12].iloc[0]
        # fastest_driver_2 = laps_driver_2[laps_driver_2['LapNumber'] == 12].iloc[0]

        # Retrieve the telemetry and add the distance column
        telemetry_driver_1 = fastest_driver_1.get_telemetry().add_distance()
        telemetry_driver_2 = fastest_driver_2.get_telemetry().add_distance()

        team_driver_1 = fastest_driver_1['Team']
        team_driver_2 = fastest_driver_2['Team']

        delta_time, ref_tel, compare_tel = utils.delta_time(fastest_driver_1, fastest_driver_2)
        plot_title = f"{sess.event.year} {sess.event.EventName} - {sess.name} - {driver_1} VS {driver_2}"


        import plotly.subplots as sp
        import plotly.graph_objects as go

        # Create subplots with different sizes
        fig = sp.make_subplots(rows=7, cols=1, subplot_titles=('', '', '', '', '', '', ''), shared_xaxes=True)

        # Delta line
        fig.add_trace(go.Scatter(x=ref_tel['Distance'], y=delta_time, name=f"Gap to {driver_2} (s)"), row=1, col=1)
        fig.add_trace(go.Scatter(x=ref_tel['Distance'], y=[0] * len(ref_tel['Distance']), name='Zero line',
                                 line=dict(color='black')), row=1, col=1)

        driver_1_color, driver_2_color = get_two_driver_plot_color(driver_1, driver_2, sess)

        # Speed trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['Speed'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=2, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['Speed'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=2, col=1)

        # Throttle trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['Throttle'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=3, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['Throttle'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=3, col=1)

        # Brake trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['Brake'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=4, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['Brake'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=4, col=1)

        # Gear trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['nGear'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=5, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['nGear'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=5, col=1)

        # RPM trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['RPM'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=6, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['RPM'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=6, col=1)

        # DRS trace
        fig.add_trace(go.Scatter(x=telemetry_driver_1['Distance'], y=telemetry_driver_1['DRS'], name=driver_1,
                                 line=dict(color=driver_1_color)), row=7, col=1)
        fig.add_trace(go.Scatter(x=telemetry_driver_2['Distance'], y=telemetry_driver_2['DRS'], name=driver_2,
                                 line=dict(color=driver_2_color)), row=7, col=1)

        # Update axis titles
        fig.update_yaxes(title_text="Gap to {} (s)".format(driver_2), row=1, col=1, anchor='free')
        fig.update_yaxes(title_text="Speed", row=2, col=1, anchor='free')
        fig.update_yaxes(title_text="Throttle", row=3, col=1, anchor='free')
        fig.update_yaxes(title_text="Brake", row=4, col=1, anchor='free')
        fig.update_yaxes(title_text="Gear", row=5, col=1, anchor='free')
        fig.update_yaxes(title_text="RPM", row=6, col=1, anchor='free')
        fig.update_yaxes(title_text="DRS", row=7, col=1, anchor='free')

        # Update layout
        fig.update_layout(title=plot_title, height=1000, showlegend=False, title_x=0.5, plot_bgcolor="white")
        fig.update_yaxes(showline=True, linecolor='black',
                         gridcolor='lightgrey')
        fig.update_xaxes(showline=True, linecolor='black', gridcolor='lightgrey')
        # Show the plot
        return fig.to_json()


