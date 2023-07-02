import json

import plotly.graph_objs as go
import requests


def _throttle_brake_drs(state, driver):
    standings = 'http://localhost:5000/v1/visualizations/throttle_brake_drs/plot'
    config = json.dumps({
        "driver":  driver,
        "year": state["year_driver_duel"],
        "GP": state["gp_driver_duel"],
        "mode": state["mode_driver_duel"]
    })

    data = requests.post(standings, timeout=8000, data=config)
    data  = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    return fig


def _fastest_per_sector(state):
    standings = 'http://localhost:5000/v1/visualizations/fastest_per_sector/plot'
    config = json.dumps({
        "year":  state["year_driver_duel"],
        "gp": state["gp_driver_duel"],
        "mode": state["mode_driver_duel"],
        "driver_a": state["driver_a"],
        "driver_b": state["driver_b"]
    })
    data = requests.post(standings, timeout=8000, data=config)
    data  = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    return fig
    #state["throttle_brake_drs_driver1"] = data


def _driver_duel_telemetry(state):
    standings = 'http://localhost:5000/v1/visualizations/driver_duel_telemetry/plot'
    config = json.dumps({
        "driver_1": state["driver_a"],
        "driver_2": state["driver_b"],
        "year": state["year_driver_duel"],
        "GP": state["gp_driver_duel"],
        "mode": state["mode_driver_duel"]
    })
    data = requests.post(standings, timeout=8000, data=config)
    data  = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    return fig