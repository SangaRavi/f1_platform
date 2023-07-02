from dependency_injector import containers,providers

from backend.dao.dao import TemporalContextAggregationImpl
from backend.ingestion.topspeed_st import TopSpeedSTIngestor
from backend.plot_components.driver_duel_telemetry import DriverDuelTelemetry
from backend.plot_components.fastest_per_sector import FastestPerSector
from backend.plot_components.lapgap import LapGap
from backend.ingestion.lapgaps import LapGapsIngestor
import psycopg2

from backend.plot_components.speeds import Speeds
from backend.plot_components.standings import Standings
from backend.plot_components.throttle_brake_drs import ThrottleBrakeDRS
from backend.plot_components.topspeed_st import TopSpeedST
from backend.structure.race_details import RaceDetails

import os


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    # conn_pool = providers.Singleton(
    #     pool.ThreadedConnectionPool,
    #     minconn=config.minconn,
    #     maxconn=config.maxconn,
    #     user=config.user,
    #     password=config.password,
    #     port=config.port,
    #     database=config.database,
    #     host=config.url)

    host = os.getenv("CURRENT_ENV", "localhost")

    conn_pool = providers.Singleton(
        psycopg2.connect,
        user="postgres",
        password="postgres",
        port="5432",
        database="postgres",
        host=host)

    temporal_context = providers.Singleton(TemporalContextAggregationImpl)
    dao = providers.Singleton(temporal_context, conn=conn_pool)

    lapgap = providers.Singleton(LapGap, dao=dao)
    standings = providers.Singleton(Standings, dao)
    speeds = providers.Singleton(Speeds, dao=dao)
    topspeed_st = providers.Singleton(TopSpeedST, dao=dao)
    fastest_per_sector = providers.Singleton(FastestPerSector, dao=dao)
    throttle_brake_drs = providers.Singleton(ThrottleBrakeDRS, dao=dao)
    driver_duel_telemetry = providers.Singleton(DriverDuelTelemetry, dao=dao)
    d = {"lapgap": lapgap,
         "standings": standings,
         "speeds": speeds,
         "topspeed_st": topspeed_st,
         "fastest_per_sector": fastest_per_sector,
         "driver_duel_telemetry": driver_duel_telemetry,
         "throttle_brake_drs": throttle_brake_drs}
    plotters = providers.Dict(d)

    lapgap_ingestor = providers.Singleton(LapGapsIngestor, dao=dao)
    topspeed_ingestor = providers.Singleton(TopSpeedSTIngestor, dao=dao)
    i = {"lapgap_ingestor": lapgap_ingestor, "topspeed_st_ingestor": topspeed_ingestor}
    ingestors = providers.Dict(i)

    race_details = providers.Singleton(RaceDetails)


