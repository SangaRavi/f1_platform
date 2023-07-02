import plotly.graph_objs as go
from attrs import define
from backend.dao.dao import TemporalContextAggregationImpl
import requests
import pandas as pd
import plotly.express as px

@define
class Standings:
    dao: TemporalContextAggregationImpl

    def get_metadata(self):
        return "standings"

    def plot(self, **kwargs):
        points = f"http://ergast.com/api/f1/{kwargs['year']}/driverStandings.json"
        data = requests.get(points, timeout=8000)
        driver_standings = data.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
        driver_data = []

        import fastf1
        sess = fastf1.get_session(kwargs["year"], 1, "R")
        sess.load()
        results = sess.results

        for entry in driver_standings:
            driver = entry['Driver']['givenName'] + ' ' + entry['Driver']['familyName']
            team = entry['Constructors'][0]['name']
            points = int(entry['points'])
            driver_data.append({'Driver': driver, 'Team': team, 'Points': points})

        driver_df = pd.DataFrame(driver_data)
        driver_df["LastName"] = driver_df["Driver"].apply(lambda x: x.split(" ")[-1])

        mapping = {"ü": "u", "é": "e"}

        driver_df["LastName"] = driver_df["LastName"].apply(
            lambda x: ''.join(mapping[ch] if ch in mapping else ch for ch in x))

        sess_df = sess.results[["FullName", "Abbreviation", "TeamColor", "TeamName"]]
        sess_df["LastName"] = sess_df["FullName"].apply(lambda x: x.split(" ")[-1])

        final_df = sess_df.merge(driver_df, on="LastName")
        final_df["TeamColor"] = "#" + final_df["TeamColor"]

        data = pd.DataFrame(final_df)
        data["Points"] = data["Points"].astype(int)
        data = data.sort_values(by="Points", ascending=False)

        if kwargs["mode"] == "constructor":
            cons_df = data.groupby(["Team", "TeamColor"])["Points"].sum().reset_index()
            cons_df.sort_values(by="Points", ascending=False, inplace=True)
            data = cons_df


        # Create horizontal bar plot
        fig = go.Figure(data=[
            go.Bar(
                y=data["Abbreviation"] if kwargs["mode"]=="driver" else data["Team"],
                x=data["Points"],
                orientation='h',
                text=[f"{int(val)}" for val in data["Points"]], textposition="outside",
                marker=dict(color=data["TeamColor"])
            )
        ])

        # Add points values to end of bars

        # Customize axes and title
        fig.update_layout(
            title='',
            xaxis_title='Points',
            yaxis_title='',
            yaxis=dict(autorange='reversed', showticklabels=True)
        )

        fig.update_xaxes(showticklabels=False)

        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", height=800)

        return fig.to_json()
