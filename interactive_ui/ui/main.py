import json
from datetime import timedelta

import plotly.express as px
import plotly.graph_objects as go
import requests
import streamsync as ss
import fastf1

from analytics import _update_laptime_chart, _speeds, _update_topspeedst_chart
from driver_duel import _throttle_brake_drs, _fastest_per_sector, _driver_duel_telemetry
import os
import logging
import traceback


logger = logging.getLogger(__name__)



host = os.getenv("BACKEND_ENV", "localhost")

def _standings(state, mode):
    try:
        standings = f'http://{host}:5000/v1/visualizations/standings/plot'
        logger.info("Requesting ", standings)
        config = json.dumps({
            "year": int(state["standings_year"]) if state["standings_year"] else 2023,
            "mode": mode
        })
        data = requests.post(standings, timeout=8000, data=config)
        data = json.loads(data.json())
        fig = go.Figure(data=data["data"], layout=data["layout"])
        if mode=="driver":
            state["driver_standings"] = fig
        else:
            state["constructor_standings"] = fig
    except:
        logger.info(traceback.format_exc())



def update(state, session):
    state["session"] = session
    _update_laptime_chart(state, "average")
    _update_laptime_chart(state, "fast")
    #_speeds(state)
    _update_topspeedst_chart(state)    
    state["plot_available"] = True


def update_driver_duel(state):
    state["selected_driver_1"] = state["driver_a"]
    state["selected_driver_2"] = state["driver_b"]
    state["throttle_brake_drs_driver1"] = _throttle_brake_drs(state, state["driver_a"])
    laptime_a = state["throttle_brake_drs_driver1"]["layout"]["title"]["text"]    
    state["throttle_brake_drs_driver2"] = _throttle_brake_drs(state, state["driver_b"])
    laptime_b = state["throttle_brake_drs_driver2"]["layout"]["title"]["text"]    
    state["circuit_fastest"] = _fastest_per_sector(state)
    state["laptime_driver1"] = laptime_a
    state["laptime_driver2"] = laptime_b

    lap_time_1_parts = laptime_a.split(":")
    lap_time_2_parts = laptime_b.split(":")
    lap_time_1 = timedelta(minutes=int(lap_time_1_parts[0]), seconds=float(lap_time_1_parts[1]))
    lap_time_2 = timedelta(minutes=int(lap_time_2_parts[0]), seconds=float(lap_time_2_parts[1]))

    # Calculating the difference in seconds.milliseconds
    diff_a = (lap_time_1.total_seconds() - lap_time_2.total_seconds())
    diff_b = (lap_time_2.total_seconds() - lap_time_1.total_seconds())
    if diff_a <= 0:
        diff_a = "+" + str("{:.3f}".format(diff_a))+"s"
        diff_b = "-+" + str("{:.3f}".format(diff_b))+"s"
    else:
        diff_a = "-+" + str("{:.3f}".format(diff_a))+"s"
        diff_b = "+" + str("{:.3f}".format(diff_b))+"s"

    state["diff_driver1"] = diff_a
    state["diff_driver2"] = diff_b
    state["driver_duel_telemetry"] = _driver_duel_telemetry(state)
    state["driver_duel_available"] = True


def update_standings(state):
    state["activate_standings"] = True
    _standings(state, mode="driver")
    _standings(state, mode="constructor")


def handle_input_change(state, payload):
    state["gp"] = payload



def ingest(state):
    config = json.dumps({
        "year": int(state["year"]) if state["year"] else 2023,
        "country": state["gp"],
        "mode": state["mode"]
    })
    ingest_endpoint = f'http://{host}:5000/v1/ingest/{state["ingestor"]}'
    print(ingest_endpoint)
    ingest = requests.post(ingest_endpoint, timeout=8000, data=config)
    print(ingest.json())


def _countries(year):
    countries = f'http://{host}:5000/v1/countries/{year}'
    countries = requests.get(countries, timeout=8000)
    return {item: item for item in countries.json()}


# def change_data_souce(state, session):
#     state["session"] = session
#     print(state["gp"])
#     if state["gp"]=="Spain":
#         state["fastest_laptime"] = _laptime(mode="average")
#     else:
#         state["fastest_laptime"] = _laptime(mode="fast")


# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

def _empty_plot():
    fig = px.bar(x=[],y=[])
    fig.update_yaxes(showline=True, linecolor='black', gridcolor='lightgrey')
    fig.update_xaxes(title="", showline=True, linecolor='black', gridcolor='lightgrey')
    fig.update_layout(showlegend=False, title="", title_x=0.5, plot_bgcolor='white')
    return fig


def update_value(state):
    state["test"] = ""


initial_state = ss.init_state({
    "year": 2023,
    "mode": "R",
    "gp": "Spain",
    "plot_available": False,
    "Driver1": "Max Verstappen",
    "Driver2": "Fernando Alonso",
    "driver_a": "VER",
    "driver_b": "ALO",
    "year_driver_duel": 2022,
    "gp_driver_duel": "Austria",
    "mode_driver_duel": "R",
    "standings_year": 2023

})

#update(initial_state, None)