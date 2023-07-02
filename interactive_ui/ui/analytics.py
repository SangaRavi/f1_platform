import json

import requests
import plotly.graph_objs as go


def _update_laptime_chart(state, mode):
    endpoint = 'http://localhost:5000/v1/visualizations/lapgap/plot'
    config = json.dumps({
        "year": int(state["year"]) if state["year"] else 2023,
        "country": state["gp"],
        "mode": state["mode"]
    })
    data = requests.post(endpoint, timeout=8000, data=config)
    data = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    if mode == "fast":
        state["fastest_laptime"] = fig
    else:
        state["average_laptime"] = fig


def _update_topspeedst_chart(state):
    endpoint = 'http://localhost:5000/v1/visualizations/topspeed_st/plot'
    config = json.dumps({
        "year": int(state["year"]) if state["year"] else 2023,
        "country": state["gp"],
        "mode": state["mode"]
    })
    data = requests.post(endpoint, timeout=8000, data=config)
    data = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    state["topspeed_st"] = fig


def _speeds(state):
    endpoint = 'http://localhost:5000/v1/visualizations/speeds/plot'
    config = json.dumps({
        "year": int(state["year"]) if state["year"] else 2023,
        "country": state["gp"],
        "mode": state["mode"]
    })
    data = requests.post(endpoint, timeout=8000, data=config)
    data = json.loads(data.json())
    fig = go.Figure(data=data["data"], layout=data["layout"])
    state["average_speed"] = fig