import psycopg2.pool as pool
from dependency_injector import containers,providers

from backend.dao.dao import TemporalContextAggregationImpl
from backend.plot_components.lapgap import LapGap
from backend.ingestion.lapgaps import LapGapsIngestor
import psycopg2

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

    conn_pool = providers.Singleton(
        psycopg2.connect,
        user="postgres",
        password="postgres",
        port="5432",
        database="postgres",
        host="localhost")

    temporal_context = providers.Singleton(TemporalContextAggregationImpl)
    dao = providers.Singleton(temporal_context, conn=conn_pool)
    lapgap = providers.Singleton(LapGap, dao=dao)
    d = {"lapgap": lapgap}
    plotters = providers.Dict(d)
    lapgap_ingestor = providers.Singleton(LapGapsIngestor, dao=dao)
    i = {"lapgap_ingestor": lapgap_ingestor}
    ingestors = providers.Dict(i)

