This is a hobby project of mine where I take data provided by fastf1 and create insights and visualizations which then I share on Twitter @ https://x.com/sangaF1Insights.

The prototype here contains 3 main components,

- An UI built with streamsync
- Visualiations integrated with UI via fastapi
- DAO to ingest, read data from Postgres Datasource

The prototype is also dockerized and a simple docker-compose up from main folder should start the app containers and publish the frontend on localhost:8501
