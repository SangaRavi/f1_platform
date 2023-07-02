import json

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import requests
import os

backend_env = os.getenv("BACKEND_ENV", "localhost")


def _standings(state, mode):
    standings = f'http://{backend_env}:5000/v1/visualizations/standings/plot'
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


def _standings_table(mode):
    standings = f'http://{backend_env}:5000/v1/visualizations/standings/plot'
    config = json.dumps({
        "year": 2023,
        "country": "Spain",
        "mode": "R"
    })
    data = requests.post(standings, timeout=8000, data=config)
    data = pd.DataFrame(json.loads(data.json()))
    data["Points"] = data["Points"].astype(int)
    data = data.sort_values(by="Points", ascending=False)
    return data
